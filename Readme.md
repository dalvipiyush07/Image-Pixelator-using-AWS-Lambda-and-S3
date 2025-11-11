# Image Pixelator using AWS Lambda and S3

## Overview

The Image Pixelator project is a simple and smart AWS-based application that automatically pixelates images. 
When a user uploads an image to an Amazon S3 bucket, an AWS Lambda function is triggered. 
The function processes the image and creates several pixelated versions in different resolutions such as 8x8, 16x16, 32x32, 48x48, and 64x64. 
All the processed images are saved in another S3 bucket for easy access. 
This project demonstrates how serverless technology can automate image processing without using any traditional servers.

![](./img/Gemini_Generated_Image_g1admxg1admxg1ad.png)


---

## What This Project Does

1. You upload an image to the source S3 bucket.
2. The Lambda function starts automatically.
3. It makes many pixelated copies of your image (like 8x8, 16x16, 32x32, etc.).
4. The pixelated images are saved in another S3 bucket.



---

## AWS Services Used

| AWS Service | Use |
|--------------|-----|
| AWS Lambda | Runs the image pixelation code automatically |
| Amazon S3 | Stores your original and processed (pixelated) images |
| AWS IAM | Gives permission to Lambda to access S3 |
| Amazon CloudWatch | Shows logs and helps check errors or performance |

---

## Steps to Set Up

### Step 1: Create Two S3 Buckets
- Source Bucket: my-source-images-bucket-piyush
- Processed Bucket: my-pixelated-images-bucket-piyush

### Step 2: Create IAM Role
Make a new role called image-pixelator-role.
Give it these permissions:
- AmazonS3FullAccess
- AWSLambdaBasicExecutionRole

### Step 3: Create Lambda Function
- Function name: image-pixelator
- Runtime: Node.js 22.x
- Architecture: x86_64
- Execution role: image-pixelator-role

Add this environment variable:
```
Key: processed_bucket
Value: my-pixelated-images-bucket-piyush
```

### Step 4: Add S3 Trigger
- Go to Lambda > Add Trigger
- Select S3 as trigger type
- Choose source bucket (my-source-images-bucket-piyush)
- Event type: All object create events

---

## How It Works

1. You upload an image like get.jpg to the source bucket.
2. Lambda runs automatically and downloads that image.
3. The function pixelates the image in different sizes (8x8 to 64x64).
4. It uploads all pixelated versions to the processed bucket.

---

## Example

Source Bucket: my-source-images-bucket-piyush/get.jpg

![](./img/get.jpg)

Processed Bucket: my-pixelated-images-bucket-piyush/
```
![](./img/pixelated-48x48-get%20(1).jpg)
```

Each file is more pixelated (blurred) than the one before.

---

## Checking Logs

You can open CloudWatch Logs to see:
- If the function worked successfully
- How long it took
- Any errors if something failed

---

## Benefits

- No servers needed (completely serverless)
- Works automatically on every image upload
- Saves time and effort
- Low cost and easy to scale

---

## Future Ideas

- Send an SMS or email when pixelation is done
- Let users choose pixel size
- Add watermark or image resize options
- Create a simple web interface for upload

---

## Author

**Piyush Dalvi**
Cloud | DevOps | AWS | Serverless Projects
[GitHub Profile](https://github.com/dalvipiyush07)

---

## Conclusion

This project shows how to use AWS Lambda, S3, and IAM to build an automatic image-processing system.
It is simple, fast, and completely serverless — great for learning AWS automation.
