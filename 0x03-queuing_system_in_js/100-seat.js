import express from "express";
import util from "util";
import { createClient } from "redis";
import { createQueue } from "kue";

const client = createClient();

function reserveSeat(number) {
  client.set("available_seats", number);
}

client.get = util.promisify(client.get);

async function getCurrentAvailableSeats() {
  const seats = await client.get("available_seats").then((value) => value);

  return seats;
}

let reservationEnabled = true;

reserveSeat(50);

const queue = createQueue();

const app = express();

app.get("/available_seats", async (req, res) => {
  const available_seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: available_seats });
});

app.get("/reserve_seat", (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: "Reservation are blocked" });
    return;
  }

  const job = queue.createJob("reserve_seat", { number: 1 }).save((err) => {
    if (err) res.json({ status: "Reservation failed" });
    else res.json({ status: "Reservation in process" });
  });

  job
    .on("complete", (result) => {
      console.log(`Seat reservation job ${job.id} completed`);
    })
    .on("failed", (errorMessage) => {
      console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
    });
});

app.get("/process", async (req, res) => {
  res.json({ status: "Queue processing" });
  queue.process("reserve_seat", async (job, done) => {
    const available_seats = Number(await getCurrentAvailableSeats());

    if (available_seats <= 0) {
      done(new Error("Not enough seats available"));
    } else {
      const new_available_seats = available_seats - 1;

      if (new_available_seats == 0) reservationEnabled = false;

      reserveSeat(new_available_seats);
      done();
    }
  });
});

app.listen(1245);
