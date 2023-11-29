import { createQueue } from 'kue';
import { createSandbox } from 'sinon';
import {expect } from 'chai';

import createPushNotificationsJobs from './8-job.js';

const queue = createQueue();

describe('createPushNotificationsJobs', () => {
    const jobs = [
        {
            phoneNumber: "02345678463",
            message: "Hello",
        },
    ];
    const sandbox = createSandbox();

    before(() => {
        queue.testMode.enter(true);
    });

    beforeEach(() => {
        sandbox.spy(console, 'log');
    });

    afterEach(() => {
        sandbox.restore();
    });

    after( function () {
        queue.testMode.clear();
        queue.testMode.exit();
    });

    it('logs an error if jobs is not an array', () => {
        expect(() => {
            createPushNotificationsJobs(3, queue);
        }).to.throw(Error, /^Jobs is not an array$/);
    });

    it('creates a new job', (done) => {
        expect(queue.testMode.jobs.length).to.equal(0);

        createPushNotificationsJobs(jobs, queue);
        expect(queue.testMode.jobs.length).to.equal(1);
        expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
        expect(queue.testMode.jobs[0].data).to.equal(jobs[0]);

        queue.process("push_notification_code_3", () => {
            expect(
              console.log.calledWith(
                `Notification job created: ${queue.testMode.jobs[0].id}`
              )
            ).to.be.true;
            done();
          });
        });

    it("job completed", (done) => {
        queue.testMode.jobs[0].addListener("complete", () => {
            expect(
              console.log.calledWith(
                `Notification job ${queue.testMode.jobs[0].id} completed`
              )
            ).to.be.true;
          });
          queue.testMode.jobs[0].emit("complete");
          done();
    });

    it("failed job", (done) => {
          queue.testMode.jobs[0].addListener("failed", (errorMessage) => {
            expect(
              console.log.calledWith(
                `Notification job ${queue.testMode.jobs[0].id} failed: ${errorMessage}`
              )
            ).to.be.false;
          });
          queue.testMode.jobs[0].emit(
            "failed",
            new Error("Phone number is blacklisted")
          );
          done();
    });

    it("checks for job progress", (done) => {
        queue.testMode.jobs[0].addListener("progress", (progress) => {
            expect(
              console.log.calledWith(
                `Notification job ${queue.testMode.jobs[0].id} ${progress}% complete`
              )
            ).to.be.true;
          });
          queue.testMode.jobs[0].emit("progress", 50);
          done();
    });
    });
