import os
import json
import uuid
import boto3
from botocore.exceptions import ClientError
from PIL import Image
from urllib.parse import unquote_plus

# Bucket names
processed_bucket = "my-pixelated-images-bucket-piyush"
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    print("=== IMAGE PIXELATION STARTED ===")
    
    try:
        # Extract S3 information from event
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        key = unquote_plus(event['Records'][0]['s3']['object']['key'])  # URL decode
        
        print(f"Source Bucket: {source_bucket}")
        print(f"Image Key: {key}")
        
        # Generate unique names for processing
        object_key = str(uuid.uuid4()) + '-' + os.path.basename(key)
        img_download_path = f'/tmp/{object_key}'
        
        # Step 1: Download image from S3
        print("Downloading image from S3...")
        with open(img_download_path, 'wb') as img_file:
            s3_client.download_fileobj(source_bucket, key, img_file)
        print("✓ Image downloaded successfully")
        
        # Step 2: Pixelate in different resolutions
        print("Starting pixelation process...")
        
        pixelate((8, 8), img_download_path, f'/tmp/pixelated-8x8-{object_key}')
        print("✓ 8x8 pixelation completed")
        
        pixelate((16, 16), img_download_path, f'/tmp/pixelated-16x16-{object_key}')
        print("✓ 16x16 pixelation completed")
        
        pixelate((32, 32), img_download_path, f'/tmp/pixelated-32x32-{object_key}')
        print("✓ 32x32 pixelation completed")
        
        pixelate((48, 48), img_download_path, f'/tmp/pixelated-48x48-{object_key}')
        print("✓ 48x48 pixelation completed")
        
        pixelate((64, 64), img_download_path, f'/tmp/pixelated-64x64-{object_key}')
        print("✓ 64x64 pixelation completed")
        
        # Step 3: Upload pixelated images to destination bucket
        print("Uploading pixelated images...")
        
        s3_client.upload_file(f'/tmp/pixelated-8x8-{object_key}', processed_bucket, f'pixelated-8x8-{os.path.basename(key)}')
        s3_client.upload_file(f'/tmp/pixelated-16x16-{object_key}', processed_bucket, f'pixelated-16x16-{os.path.basename(key)}')
        s3_client.upload_file(f'/tmp/pixelated-32x32-{object_key}', processed_bucket, f'pixelated-32x32-{os.path.basename(key)}')
        s3_client.upload_file(f'/tmp/pixelated-48x48-{object_key}', processed_bucket, f'pixelated-48x48-{os.path.basename(key)}')
        s3_client.upload_file(f'/tmp/pixelated-64x64-{object_key}', processed_bucket, f'pixelated-64x64-{os.path.basename(key)}')
        
        print("✓ All pixelated images uploaded successfully")
        print("=== IMAGE PIXELATION COMPLETED ===")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully processed and uploaded pixelated images!')
        }
        
    except Exception as e:
        print(f"=== ERROR: {str(e)} ===")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Processing failed: {str(e)}')
        }

def pixelate(pixelsize, image_path, pixelated_img_path):
    """Pixelate the image to specified pixel size"""
    # Open original image
    img = Image.open(image_path)
    
    # Get original dimensions
    original_size = img.size
    
    # Resize to small pixels and scale back to original size
    temp_img = img.resize(pixelsize, Image.BILINEAR)
    pixelated_img = temp_img.resize(original_size, Image.NEAREST)
    
    # Save pixelated image
    pixelated_img.save(pixelated_img_path)
