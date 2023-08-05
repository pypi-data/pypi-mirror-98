import importlib
import io
import numpy as np
import pandas as pd
from astropy.io import ascii
from astropy.io.votable import parse,parse_single_table,from_table, writeto
from astropy.io.votable.tree import VOTableFile, Resource, Table, Field
from astropy.table import Table, Column
from Freya_alerce.files.verify_file import Verify

"""
Class to get data from module catalog configured in Freya, first check if catalog exist inside Freya
and if not exist try import catalog from local folder. The data get is all ligh curve of object in area use
degrees (ra,dec,radius) or use the format hh:mm:ss (hh:mm:ss,radius).
Other option is get the only light curve of object most close to area selected.
"""
class GetData(object):
    """
    Parameters
    -------------------------------------- 
    ra : (float) 
        (degrees) Right Ascension
    dec : (float) 
        (degrees) Declination 
    hms : (string)
        format ICRS (hh:mm:ss)
    radius : (float)
        Search radius
    format : (string)
        [numpy,csv,votable]
    catalog: (string)
        Catalog to search
    """

    def __init__(self,radius=0.0002777,format='numpy',nearest=False,**kwargs):
        self.catalog = kwargs.get('catalog').strip().upper()
        #self.catalog = self.catalog.replace(self.catalog[0],self.catalog[0].upper(),1)
        self.ra = kwargs.get('ra')
        self.dec = kwargs.get('dec')
        self.hms = kwargs.get('hms')
        self.radius = radius
        self.format = format
        self.nearest = nearest

        if self.format not in ['csv','votable']:
             return "inadmissible format in consult data"
    

    def generic_call_data(self,call_method):
        """
        Get the LC of catalog called in format CSV/VOTable. 
        Return
        -------
        Columns : ['obj','ra','dec','mjd','mag','filter','catalog'].
            obj : double
                Id of object in catalog
            ra : float
                Right ascension
            dec : float
                Declination
            mjd : float
                Julian day
            mag : float
                Magnitud
            magerr : float
                Magnitud error
            filter : str
                Band
            catalog : str
                Catalog source
        """
        try :
            """
            Search catalog insiede Freya, if not exist search inside local folder.
            """
            if Verify().verify_catalog_inside(self.catalog):
                module = f'Freya_alerce.catalogs.{self.catalog}.configure'
            elif Verify().verify_catalog_local(self.catalog) :
                 module = f'{self.catalog}.configure'

            # Import self.catalog
            mod = importlib.import_module(module)
            # Call class
            class_ =  getattr(mod,f'Configure{self.catalog}') 
            # Call method especific of class
            if call_method == 'get_lc_deg':
                method_ = class_(ra=self.ra,dec=self.dec,radius=self.radius,nearest=self.nearest).get_lc_deg()      
            elif call_method == 'get_lc_hms':
                method_ = class_(hms=self.hms,radius=self.radius,nearest=self.nearest).get_lc_hms()
            # set de estructure return with format
            if self.format == 'numpy':
                row_catalog = np.full(method_.shape[0],self.catalog)
                method_ = np.column_stack((method_, row_catalog))
                return method_
            elif self.format == 'csv':
                row_catalog = np.full(method_.shape[0],self.catalog)
                df = pd.DataFrame({'obj':method_[:,0],'ra':method_[:,1],
                                    'dec':method_[:,2],'mjd':method_[:,3],
                                    'mag':method_[:,4],'magerr':method_[:,5],
                                    'filter':method_[:,6],'catalog':row_catalog})
                return df.to_csv(index=False)
            elif self.format == 'votable':
                row_catalog = np.full(method_.shape[0],self.catalog)
                method_ = np.column_stack((method_, row_catalog))
                names_column = ['obj','ra','dec','mjd','mag','magerr','filter','catalog']
                descriptions_column = ['Id of object in catalog the original catalog',
                                        'Right ascension','Declination',
                                        'Julian Day','Magnitude','Magnitude Error',
                                        'Filter code','Original Catalog']
                #dtype_column = [] # dtype=dtype_column
                t = Table(rows=method_,names=names_column,descriptions=descriptions_column)
                votable= VOTableFile.from_table(t)
                buf = io.BytesIO()
                writeto(votable,buf)
                return buf.getvalue().decode("utf-8")
        except :
            print(f'No find the catalog : {self.catalog}')