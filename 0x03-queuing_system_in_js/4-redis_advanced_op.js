import { createClient, print } from 'redis';

const client = createClient();

client.on('connect', () => {
    console.log('Redis client connected to the server');
});
const obj = {
    portland: 50,
    Seattle: 80,
    'New York': 20,
    Bogota: 20,
    Cali: 40,
    Paris: 2
}

for (const  [field, value] of Object.entries(obj)) {
    client.HSET('HolbertonSchools', field, value, print);
};

client.HGETALL('HolbertonSchools', (err, reply) => {
    console.log(reply);
});
