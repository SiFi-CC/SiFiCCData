from django import template    
register = template.Library()    

@register.filter('timestamp_to_time')
def convert_timestamp_to_time(timestamp):
    import datetime
    dt = datetime.datetime.fromtimestamp(int(timestamp))
    return dt.strftime('%Y-%m-%d %H:%M:%S')
