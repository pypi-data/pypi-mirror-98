# =============================================================================
# step23.py부터 step32.py까지는 simple_core를 이용해야 합니다.
is_simple_core = False  # True
# =============================================================================

if is_simple_core:
    from hj_dezero.core_simple import Variable
    from hj_dezero.core_simple import Function
    from hj_dezero.core_simple import using_config
    from hj_dezero.core_simple import no_grad
    from hj_dezero.core_simple import as_array
    from hj_dezero.core_simple import as_variable
    from hj_dezero.core_simple import setup_variable

else:
    from hj_dezero.core import Variable
    from hj_dezero.core import Parameter
    from hj_dezero.core import Function
    from hj_dezero.core import using_config
    from hj_dezero.core import no_grad
    from hj_dezero.core import test_mode
    from hj_dezero.core import as_array
    from hj_dezero.core import as_variable
    from hj_dezero.core import setup_variable
    from hj_dezero.core import Config
    from hj_dezero.layers import Layer
    from hj_dezero.models import Model
    from hj_dezero.datasets import Dataset
    from hj_dezero.dataloaders import DataLoader
    from hj_dezero.dataloaders import SeqDataLoader

    import hj_dezero.datasets
    import hj_dezero.dataloaders
    import hj_dezero.optimizers
    import hj_dezero.functions
    import hj_dezero.functions_conv
    import hj_dezero.layers
    import hj_dezero.utils
    import hj_dezero.cuda
    import hj_dezero.transforms

setup_variable()
__version__ = '0.0.13'
