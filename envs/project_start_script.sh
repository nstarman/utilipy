
###############################################################################
### Notes
#
#
#
###############################################################################


###############################################################################
### PARAMETERS

# get name of virtual environment
read -p "Environment name: " env_name  # get input from user

# whether to make default environment in this folder
source ./main_env.sh
if [ -z "$main_env" ]
then
    echo main_env=$env_name > ./main_env.sh
else
 #    echo "make project's main ipython environment?"
 #    select make_main in "Yes" "No"; do
	# 	case $make_main in  
	# 		Yes ) echo main_env="${env_name}" > main_env.sh; break;; 
	# 		No ) echo kept $main_env; exit;; 
	# 	esac
	# done
	while true; do
	    read -p "make project's main ipython environment? [y, N]: " yn
	    case $yn in
	        [Yy]* ) echo main_env="${env_name}" > main_env.sh; break;;
	        [Nn]* ) echo "kept ${main_env}"; exit;;
	        * ) echo "Please answer yes or no.";;
	    esac
	done
fi

###############################################################################
### ENVIRONMENT SETUP

# make directory for this environment
mkdir $env_name

# set environment.yml name field
sed "1s/.*/name: ${env_name}/" environment_pre.txt > ${env_name}_environment.yml
echo "made ${env_name} environment.yml file"

# create environment
conda env create -f ${env_name}_environment.yml -p $env_name --json --verbose

# change name from full path to just $env_name
conda config --set env_prompt '({name})'
echo "configured conda environment name"

# install into environment
# python ../setup.py install

###############################################################################
## IPYTHON

# install env into ipython
# echo "install env into ipython?"
# select make_main in "y" "n"; do
# 	case $ipy_install in  
# 	  y) ipython kernel install --user --name=$env_name; break ;; 
# 	  n) echo "not installed"; exit ;; 
# 	esac
# done
while true; do
    read -p "install env into ipython? [y, N]: " yn
    case $yn in
        [Yy]* ) ipython kernel install --user --name=$env_name; break;; 
        [Nn]* ) echo "not installed"; exit;; 
        * ) echo "Please answer yes or no.";;
    esac
done

# TODO Ipython profile configuration


###############################################################################
## TEST

source activate ./$env_name

###############################################################################
### END
