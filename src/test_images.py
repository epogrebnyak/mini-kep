import pytest
import tempfile
import os


from images import Spline
from images import IndicatorChart
import getter

@pytest.fixture    
def tempdir():
    yield tempfile.mktemp()


dfm = getter.get_dataframe('m')
ts = dfm['RETAIL_SALES_FOOD_bln_rub']

class Test_Spline:
    
    def setup_method(self):        
        self.graph = Spline(ts)

    def test_show(self):
        self.graph.show()

    def test_save(self, tempdir):
        folder = tempdir 
        self.graph.save(folder)
        filepath = self.graph.get_path()
        assert os.path.exists(filepath)


class Test_IndicatorChart(Test_Spline):
    
    def setup_method(self):
        self.graph = IndicatorChart(ts)


if __name__ == "__main__":
    pytest.main([__file__])


