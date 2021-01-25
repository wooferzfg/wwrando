DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $DIR

key_1=$(python3 -m generate_key.py)
key_2=$(python3 -m generate_key.py)
key_3=$(python3 -m generate_key.py)
key_4=$(python3 -m generate_key.py)

echo -n "SEED_KEY=['0X$key_1','0X$key_2','0X$key_3','0X$key_4']" > $DIR/seed_key.py

echo $(python3 -m generate_key.py) > $DIR/build_key.txt
