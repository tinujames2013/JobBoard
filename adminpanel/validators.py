from django.core.exceptions import ValidationError

def validate_file_type(file):
    if not file:
        return  # Skip validation if no file is provided
    
    try:
        content_type = file.content_type
    except AttributeError:
        raise ValidationError("Invalid file. Please upload a valid file.")
    
    allowed_types = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ]
    
    if content_type not in allowed_types:
        raise ValidationError(
            f"Unsupported file type: {content_type}. Only PDF and Word documents are allowed."
        )
