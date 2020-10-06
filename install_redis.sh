# run with sudo privilege

# install
redisurl="http://download.redis.io/redis-stable.tar.gz"
curl -s -o redis-stable.tar.gz $rudisurl
# sudo su root
mkdir -p /usr/local/lib/
chmod a+w /usr/local/lib/
tar -C /usr/local/lib/ -xzf redis-stable.tar.gz
rm redis-stable.tar.gz
rm dump.rdb
cd /usr/local/lib/redis-stable/
make && make install

# configure
mkdir -p /etc/redis/
touch /etc/redis/6379.conf
echo """
port              6379
daemonize         yes
save              60 1
bind              127.0.0.1
tcp-keepalive     300
dbfilename        dump.rdb
dir               ./
rdbcompression    yes
""" > /etc/redis/6379.conf
