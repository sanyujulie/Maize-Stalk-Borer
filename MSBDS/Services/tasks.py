from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from Services.models import CustomUser, Client, DomainService, SSLCertificateService, LicenseService, InsuranceService, Subscription


@shared_task
def send_expiry_reminder_notification():
    expiry_date_threshold = datetime.now() + timedelta(days=60)
    
    # Get users with department "Welfare/Operations"
    welfare_users = CustomUser.objects.filter(department='Welfare/Operations')

    
    subscriptions = Subscription.objects.filter(expiry_date__lte=expiry_date_threshold)
    insurances = InsuranceService.objects.filter(expiry_date__lte=expiry_date_threshold)

    for user in welfare_users:
        # Send notifications for Subscription and InsuranceService to Welfare/Operations users
        recipient_email = user.email
        
        subscription_subject = 'Subscription Expiry Reminder'
        subscription_messages = []
        for subscription in subscriptions:        
            subsc_message = f"{subscription.provider}'s subscription will expire on {subscription.expiry_date}."
            subscription_messages.append(subsc_message)
            
        subscription_message = "Hello,\n" + "The following services are about to expire: \n\n" + "\n".join(subscription_messages) + "\n\n" + "Please renew your subscription to continue using our services."
        send_mail(subscription_subject, subscription_message, settings.EMAIL_HOST_USER, [recipient_email])


        insurance_subject = 'Insurance Expiry Reminder'
        insurance_messages = []
        for insurance in insurances:        
            insu_message = f'{insurance.insurance_type} insurance will expire on {insurance.expiry_date}.'
            insurance_messages.append(insu_message)
            
        insurance_message = "Hello,\n" + "The following services are about to expire: \n\n" + "\n".join(insurance_messages) + "\n\n" + "Please renew your insurance to stay covered."
        send_mail(insurance_subject, insurance_message, settings.EMAIL_HOST_USER, [recipient_email])



    # Get users with other departments
    other_users = CustomUser.objects.filter(department__in=['IT', 'Management'])

    # Get subscriptions expiring within the threshold for other users
    other_subscriptions = Subscription.objects.filter(expiry_date__lte=expiry_date_threshold)
    other_insurances = InsuranceService.objects.filter(expiry_date__lte=expiry_date_threshold)
    clients = Client.objects.filter(expiry_date__lte=expiry_date_threshold)
    domain_services = DomainService.objects.filter(expiry_date__lte=expiry_date_threshold)
    ssl_certificates = SSLCertificateService.objects.filter(expiry_date__lte=expiry_date_threshold)
    licenses = LicenseService.objects.filter(expiry_date__lte=expiry_date_threshold)

    for user in other_users:
        recipient_email = user.email
        
        subscription_subject = 'Subscription Expiry Reminder'
        subscription_messages = []
        for subscription in other_subscriptions:        
            subsc_message = f"{subscription.provider}'s subscription will expire on {subscription.expiry_date}."
            subscription_messages.append(subsc_message)
            
        subscription_message = "Hello,\n" + "The following services are about to expire: \n\n" + "\n".join(subscription_messages) + "\n\n" + "Please renew your subscription to continue using our services."
        send_mail(subscription_subject, subscription_message, settings.EMAIL_HOST_USER, [recipient_email])


        insurance_subject = 'Insurance Expiry Reminder'
        insurance_messages = []
        for insurance in other_insurances:        
            insu_message = f'{insurance.insurance_type} insurance will expire on {insurance.expiry_date}.'
            insurance_messages.append(insu_message)
            
        insurance_message = "Hello,\n" + "The following services are about to expire: \n\n" + "\n".join(insurance_messages) + "\n\n" + "Please renew your insurance to stay covered."
        send_mail(insurance_subject, insurance_message, settings.EMAIL_HOST_USER, [recipient_email])

        cli_subject = 'Payment Status Reminder'
        client_messages = []
        for client in clients:       
            cli_message = f"{client.company_name}'s Payment Status will expire on {client.expiry_date}."
            client_messages.append(cli_message)

        client_message = "Hello,\n" + "The following services are about to expire: \n\n" + "\n".join(client_messages) + "\n\n" + "Please renew your payment to stay covered."
        send_mail(cli_subject, client_message, settings.EMAIL_HOST_USER, [recipient_email])

        dom_subject = 'Domain Expiry Reminder'
        domain_messages = []
        for domain_service in domain_services:       
            dom_message = f'{domain_service.domain_name} domain will expire on {domain_service.expiry_date}.'
            domain_messages.append(dom_message)

        domain_message = "Hello,\n" + "The following services are about to expire: \n\n" + "\n".join(domain_messages) + "\n\n" + "Please renew your Domain to continue using our services."
        send_mail(dom_subject, domain_message, settings.EMAIL_HOST_USER, [recipient_email])

        ssl_subject = 'Domain Expiry Reminder'
        ssl_certificate_messages = []
        for ssl_certificate in ssl_certificates:       
            ssl_cert = f'{ssl_certificate.sub_domain} SSL will expire on {ssl_certificate.expiry_date}.'
            ssl_certificate_messages.append(ssl_cert)

        ssl_message = "Hello,\n" + "The following services are about to expire: \n\n" + "\n".join(ssl_certificate_messages) + "\n\n" + "Please renew your SSL Certificate to continue using our services."
        send_mail(ssl_subject, ssl_message, settings.EMAIL_HOST_USER, [recipient_email])


        lcns_subject = 'License Expiry Reminder'
        license_messages = []
        for license in licenses:      
            lcns_message = f'{license.license_name} license service will expire on {license.expiry_date}.'
            license_messages.append(lcns_message)

        domain_message = "Hello,\n" + "The following services are about to expire: \n\n" + "\n".join(license_messages) + "\n\n" + "Please renew your License to stay covered."
        send_mail(lcns_subject, domain_message, settings.EMAIL_HOST_USER, [recipient_email])
