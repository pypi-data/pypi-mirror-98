from pprint import pprint
import tensorflow.keras as keras
from . import load
from . import blocks
import tfbox.utils.helpers as h


# 
# Model: Parent class for TBox models/blocks
# 
# a simple wrapper of keras.Model with the following additions:
#
#   - an optional classifier
#   - is_skip property 
#   - standardized naming for tfbox models/blocks  
# 
class Model(keras.Model):
    #
    # CONSTANTS
    #
    NAME='TFBoxModel'
    DEFAULT_KEY=NAME
    SEGMENT='segment'
    GLOBAL_POOLING='global_pooling'
    DEFAULT_CLASSIFIER=SEGMENT


    #
    # PUBLIC
    #
    def __init__(self,
            is_skip=False,  
            name=NAME,
            named_layers=True,
            noisy=True):
        super(Model, self).__init__()
        self.classifier=None
        self.is_skip=is_skip
        self.model_name=name
        self.named_layers=named_layers


    def set_classifier(self,
            nb_classes,
            config,
            file_name='classifier',
            folder=load.TFBOX,
            from_logits=None):
        if from_logits in [True,False]:
            config=self._update_activation(config,from_logits)
        if nb_classes and config:
            if config is True:
                config={}
            elif isinstance(config,str):
                config={ 'classifier_type': config }
            else:
                config=load.config(config,file_name,folder)
            classifier_type=config.pop( 'classifier_type', self.DEFAULT_CLASSIFIER )
            if classifier_type==Model.SEGMENT:
                self.classifier=blocks.SegmentClassifier(
                    nb_classes=nb_classes,
                    **config)
            elif classifier_type==Model.GLOBAL_POOLING:
                raise NotImplementedError('TODO: GAPClassifier')
            else:
                raise NotImplementedError(f'{classifier_type} is not a valid classifier')
        else:
            self.classifier=False

        
    def output(self,x):
        if self.classifier:
            x=self.classifier(x)
        return x


    def layer_name(self,group=None,index=None):
        return blocks.layer_name(self.model_name,group,index=index,named=self.named_layers)


    def _update_activation(self,config,from_logits):
        if config is True:
            config={}
        if config is False:
            config={
                'filters': False
            }
        config['output_act']=not from_logits
        return config



