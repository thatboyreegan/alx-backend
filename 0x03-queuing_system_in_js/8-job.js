

function createPushNotificationsJobs(jobs, queue) {
    if (!Array.isArray(jobs)) {
       throw new Error('Jobs is not an array');
    } else {
        jobs.forEach((job) => {
            const j = queue.createJob('push_notification_code_3', job);
            j.on('enqueue', () => {
                console.log(`Notification job created: ${j.id}`);
            });
            j.on('complete', () => {
                console.log(`Notification job ${j.id} completed`);
            });
            j.on('failed', (err) => {
                console.log(`Notification job ${j.id} failed: `, err);
            });
            j.on('progress', (progress, _data) => {
                console.log(`Notification job ${j.id} ${progress}% complete`);
            });
            j.save();
        })
    }
}

module.exports = createPushNotificationsJobs;