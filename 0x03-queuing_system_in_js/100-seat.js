import { createClient } from "redis";
import { promisify } from 'util';
import { createQueue } from 'kue';

const express = require('express');


let reservationEnabled = true;
const client = createClient();

client.GET = promisify(client.GET);

const reserveSeat = (number) => {
    client.SET('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
    const value = await client.GET('available_seats').then((reserved) => {
        if (!reserved) reserved = 0;
        return reserved;
    });
    return value;
};

reserveSeat(50);
const queue = createQueue();

const app = express();

app.get('/available_seats', async (req, res) => {
    const available_seats = await getCurrentAvailableSeats();
    res.status(200).json({numberOfAvailableSeats: available_seats});
});

app.get('/reserve_seat', (req, res) => {
    if (!reservationEnabled) {
        res.status(200).json({status: 'Reservetion are blocked'});
        return;
    };
    const job = queue.create('reserve_seat', {
        seats: 1
    }).save((_err) => {
        if(_err) {
            res.status(200).json({
                status: 'Reservation failed'
            });
            return;
        }
        res.status(200).json({
            status: 'Reservation in process'
        });
    });
    job.on('complete', () => {
        console.log(`Seat reservation job ${job.id} completed`);
    }).on('failed', (_err) => {
        console.log(`Seat reservation job ${job.id} failed: ${_err}`)
    });
});

app.get('/process', (req, res) => {

    queue.process('reserve_seat', async (job, done) => {
        const currentAvailableSeats = Number(await getCurrentAvailableSeats());
        if (currentAvailableSeats == 0) {
            done(Error('Not enough seats available'));
        } else {
            const new_seats = currentAvailableSeats - 1;
            if (new_seats == 0) reservationEnabled = false;

            reserveSeat(new_seats);
            done()
        }
    })
    res.status(200).json({
        status: 'Queue processing'
    });
})

app.listen(1245);
