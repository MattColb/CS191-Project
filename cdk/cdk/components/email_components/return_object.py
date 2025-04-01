class cdk_object:
    
    def __init__(self, verification_sqs, verification_lambda, weekly_start_lambda, weekly_email_queue, weekly_email_lambda):
        self.verification_sqs = verification_sqs
        self.verification_lambda = verification_lambda
        self.weekly_start_lambda = weekly_start_lambda
        self.weekly_notification_queue = weekly_email_queue
        self.weekly_email_lambda = weekly_email_lambda

        
    