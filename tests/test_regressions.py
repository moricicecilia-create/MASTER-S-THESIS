import copy,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.data import load_dataset
from src.validation import validate_experiment
from src.execution import completed,atomic_json,sha256,export_tables
from src.experiment import run_one_model_seed
from src.splits import make_splits
from src.preprocessing import ModelPreprocessor
from src.missingness import scenario_name,make_mask

class RegressionTests(unittest.TestCase):
    def setUp(self):self.cfg=json.loads((ROOT/'configs/experiment.json').read_text())
    def test_numeric_positive_zero(self):
        with tempfile.TemporaryDirectory() as d:
            pd.DataFrame({'x':[1,2,3,4],'y':[0,1,0,1]}).to_csv(Path(d)/'d.csv',index=False)
            _,y,_=load_dataset({'name':'d','path':'d.csv','target_column':'y','positive_class':0,'negative_class':1},Path(d))
            np.testing.assert_array_equal(y,[1,0,1,0])
    def test_multiclass_not_silently_binarized(self):
        with tempfile.TemporaryDirectory() as d:
            pd.DataFrame({'x':[1,2,3],'y':[0,1,2]}).to_csv(Path(d)/'d.csv',index=False)
            with self.assertRaises(ValueError):load_dataset({'name':'d','path':'d.csv','target_column':'y','positive_class':1,'negative_class':0},Path(d))
    def test_arff_categorical_and_missing(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'d.arff').write_text('@RELATION d\n@ATTRIBUTE x NUMERIC\n@ATTRIBUTE cat {a,b}\n@ATTRIBUTE y {no,yes}\n@DATA\n1,a,no\n?,b,yes\n3,?,no\n4,a,yes\n')
            X,y,m=load_dataset({'name':'d','path':'d.arff','format':'arff','target_column':'y','positive_class':'yes','negative_class':'no'},Path(d))
            self.assertEqual(m['original_missing_cells'],2);self.assertEqual(m['categorical_columns'],['cat'])
            prep=ModelPreprocessor('MLP',['x'],['cat']);self.assertTrue(np.isfinite(prep.fit_transform(X)).all())
    def test_imputation_ignores_heldout_values(self):
        train=pd.DataFrame({'x':[1.,3.,np.nan],'cat':['a','b',np.nan]})
        prep=ModelPreprocessor('TabPFN-v2',['x'],['cat']).fit(train)
        out=prep.transform(pd.DataFrame({'x':[np.nan,100000.],'cat':['unseen','a']}))
        self.assertEqual(out[0,0],2.)
    def test_bad_configuration_rejected(self):
        for modify in [lambda c:c['calibration'].update(methods=['typo']),lambda c:c['missingness'].update(cell_rates=[.1,.1]),lambda c:c.update(seeds=[42,42]),lambda c:c.update(threads=0)]:
            c=copy.deepcopy(self.cfg);modify(c)
            with self.assertRaises(ValueError):validate_experiment(c)
    def test_fractional_rate_name(self):self.assertEqual(scenario_name('cell',.125),'cell_12.5')
    def test_invalid_mask_rate(self):
        with self.assertRaises(ValueError):make_mask((3,4),'cell',1.5,42)
    def test_resume_integrity(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d);(path/'r.csv').write_text('x\n1\n')
            atomic_json(path/'complete.json',{'fingerprint':'a','files':{'r.csv':sha256(path/'r.csv')}})
            self.assertTrue(completed(path,'a'))
            with self.assertRaises(ValueError):completed(path,'b')
            (path/'r.csv').write_text('x\n2\n')
            with self.assertRaises(ValueError):completed(path,'a')
    def test_configurable_grid_end_to_end(self):
        # A real small MLP on mixed data: unusual rates, 12 panels, no fixed 10/30 assumptions.
        rng=np.random.default_rng(1)
        X=pd.DataFrame({'x':rng.normal(size=120),'z':rng.normal(size=120),'c':['a','b']*60})
        X.loc[::9,'x']=np.nan;y=np.array([0,1]*60)
        cfg=copy.deepcopy(self.cfg);cfg['mlp'].update(max_epochs=4,patience=2,hidden_layer_sizes=[4])
        cfg['missingness'].update(cell_rates=[.05,.125,.2,.35,.4,.6],feature_rates=[.1,.2,.4,.6,.8],augmentation_cell_rates=[.15,.45])
        cfg['calibration']['methods']=['No additional calibration','Missingness-augmented calibration']
        meta={'numeric_columns':['x','z'],'categorical_columns':['c'],'n_rows':120,'n_features':3}
        with tempfile.TemporaryDirectory() as d:
            rows,probs,status=run_one_model_seed('mixed','MLP',42,X,y,meta,make_splits(y,42,cfg['split']),cfg,d,1)
            self.assertEqual(status['status'],'success',status);self.assertEqual(len(rows),24)
            self.assertTrue(list((Path(d)/'reliability_diagrams').glob('*.png')))
            for row in rows:
                if row['calibration']=='No additional calibration':
                    self.assertEqual(row['calibration_fit_seconds'],0);self.assertEqual(row['calibration_prediction_seconds'],0)
            scenes={p['scenario'] for p in probs if p['subset']=='calibration'}
            self.assertEqual(scenes,{'reference','cell_15','cell_45'})
    def test_no_calibration_avoids_calibration_predictions(self):
        cfg=copy.deepcopy(self.cfg);cfg['calibration']['methods']=['No additional calibration'];cfg['mlp'].update(max_epochs=2,hidden_layer_sizes=[3])
        X=pd.DataFrame({'x':np.arange(80,dtype=float)});y=np.array([0,1]*40)
        with tempfile.TemporaryDirectory() as d, patch('src.experiment.save_reliability_figure'):
            rows,probs,status=run_one_model_seed('nocal','MLP',42,X,y,{'numeric_columns':['x'],'categorical_columns':[],'n_rows':80,'n_features':1},make_splits(y,42,cfg['split']),cfg,d,1)
            self.assertEqual(status['status'],'success');self.assertTrue(all(p['subset']=='test' for p in probs))

if __name__=='__main__':unittest.main()
