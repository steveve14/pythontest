# context_processors.py
def auth_context(request):
    return {
        'is_customer_authenticated': request.session.get('is_customer_authenticated', False),
        'is_business_authenticated': request.session.get('is_business_authenticated', False)
    }