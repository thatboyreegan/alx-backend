import { createQueue }  from 'kue';


const queue = createQueue({name: 'push_notification_code'});

const job = queue.create('push_notification_code', {
    phoneNumber: '07048234567',
    message: 'account created'
});

job.on('enqueue', () => {
    console.log('Notification job created:', job.id)
})

job.on('complete', () => {
    console.log('Notification job completed');
});

job.on('failed', () => {
    console.log('Notification job failed')
});
job.save();

