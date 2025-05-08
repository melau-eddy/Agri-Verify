from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator, MaxValueValidator



class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    is_agriculture_related = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}"



class GovernmentApproval(models.Model):
    APPROVAL_STATUS = [
        ('pending', 'Pending Review'),
        ('approved', 'Fully Approved'),
        ('conditional', 'Conditionally Approved'),
        ('rejected', 'Rejected'),
        ('revoked', 'Approval Revoked'),
    ]
    
    status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    approval_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    approval_id = models.CharField(max_length=50, unique=True)
    approving_body = models.CharField(max_length=200)
    risk_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        help_text="1=Lowest risk, 5=Highest risk"
    )
    conditions = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Government Approvals"

    def __str__(self):
        return f"{self.approving_body} - {self.get_status_display()}"

class EducationalVideo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(
        upload_to='educational_videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'mkv', 'webm'])],
        help_text="Upload video file (MP4, MOV, AVI, MKV, or WEBM)",
        null=True
    )
    duration = models.CharField(
        max_length=10,
        blank=True,
        help_text="Duration in format MM:SS (auto-calculated if blank)"
    )
    source = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    related_approval = models.ForeignKey(
        GovernmentApproval, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='educational_videos'
    )
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.duration and self.video_file:
            # Calculate duration from video file (requires moviepy or similar)
            try:
                from moviepy.editor import VideoFileClip
                clip = VideoFileClip(self.video_file.path)
                duration_sec = clip.duration
                self.duration = f"{int(duration_sec // 60)}:{int(duration_sec % 60):02d}"
                clip.close()
            except:
                # Fallback if moviepy not available
                self.duration = "00:00"
        
        super().save(*args, **kwargs)
    
    @property
    def video_url(self):
        return self.video_file.url if self.video_file else None
    
    

class VerifiedProduct(models.Model):
    PRODUCT_TYPES = [
        ('seed', 'Seeds'),
        ('crop', 'Crops'),
        ('processed', 'Processed Food'),
        ('animal', 'Animal Product'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    image = models.ImageField(upload_to='products/')
    manufacturer = models.CharField(max_length=200)
    approval = models.ForeignKey(GovernmentApproval, on_delete=models.PROTECT)
    date_added = models.DateTimeField(auto_now_add=True)
    gmo_traits = models.TextField()
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.qr_code and self.approval:
            self.generate_qr_code()
        super().save(*args, **kwargs)
    
    def generate_qr_code(self):
        import qrcode
        from io import BytesIO
        from django.core.files.base import ContentFile
        
        qr_data = f"""
        Product: {self.name}
        Approval ID: {self.approval.approval_id}
        Status: {self.approval.get_status_display()}
        Approved by: {self.approval.approving_body}
        Approval Date: {self.approval.approval_date}
        Expiry: {self.approval.expiry_date}
        Risk Level: {self.approval.risk_level}/5
        """
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        
        self.qr_code.save(
            f'qr_{self.approval.approval_id}.png',
            ContentFile(buffer.getvalue()),
            save=False
        )