# !/bin/bash

function add_package_by_path {
        MY_SOFTWARE_PATH=$1
        export PATH=${MY_SOFTWARE_PATH}/bin:${PATH}
        export CPATH=${MY_SOFTWARE_PATH}/include:${CPATH}
        export LIBRARY_PATH=${MY_SOFTWARE_PATH}/lib:${LIBRARY_PATH}
        export LD_LIBRARY_PATH=${MY_SOFTWARE_PATH}/lib:${LD_LIBRARY_PATH}
        export LIBRARY_PATH=${MY_SOFTWARE_PATH}/lib64:${LIBRARY_PATH}
        export LD_LIBRARY_PATH=${MY_SOFTWARE_PATH}/lib64:${LD_LIBRARY_PATH}

        #exprot PYTHONPATH
}

# export local_program_root_path=xxxx
# add_package_by_path $local_program_root_path