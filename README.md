# Optimizing AWS Costs by Identifying Unused Resources

## ❓ Challenge :
Sometimes, developers create EC2 instances with attached volumes by default and take snapshots for backup. When they no longer need the instance and delete it, they might forget to remove the snapshots. As a result, they keep paying for these unused snapshots, even though they're not needed anymore. Lets solve this problem!

## 💡Approach :
To solve the above problem, we will use a Lambda function, which will check our snapshots and EC2 instances. If the Lambda function finds a snapshot that is not linked to any active EC2 instances, it will delete the snapshot. By doing so, it will save us money and help reduce unnecessary costs. Let me show you, step by step!

## 👁 Observation :
There are many similar issues to concern, for e.g: Unused EBS Volumes(storage cost-$), Unused Load Balancers(costs for services-$), Unused Elastic IP attached with EC2 Instances($) and many more.

## 🪜 Steps :
### Step 1:
1. Log into your AWS Console, navigate to the EC2 Console, go to the Instances section, select 'Instances,' and click on 'Launch Instance'. Create a EC2 Instance (I am using Free Tier). <br>

   ![image](https://github.com/user-attachments/assets/2c31f619-685b-4dd6-8c44-ef1724d45d71)<br><br>

2. Navigate to the 'Elastic Block Store' section, select 'Volumes,' and observe the default volume that has been automatically created.<br>

    ![image](https://github.com/user-attachments/assets/4c549dfa-6489-4732-a0d0-e38ce736eafb)<br><br>

3. Go to the 'Snapshots' section, click 'Create Snapshot,' set 'Resource type' to 'Volume,' and choose the automatically created volume from the 'Volume ID' dropdown. Finally, click the 'Create Snapshot' button. <br>

    ![image](https://github.com/user-attachments/assets/72ce7922-cadc-46fe-84db-449bd1a37348)<br><br>

### Step 2 :
1. Navigate to the 'Lambda Console', click on 'Functions,' select 'Author from Scratch,' enter a Function name, choose the latest Python version, scroll down, and click 'Create Function'. <br>

    ![image](https://github.com/user-attachments/assets/2a8a036d-8623-43bc-b25d-e26de2f25c24) <br><br>

2. After creating the function, scroll down to the Code section, clear the existing code, replace it with 'Python_script_CleanEBS.py', then click Deploy to save your changes. Finally, click Test, which will prompt a page similar to the image below. <br>

    ![image](https://github.com/user-attachments/assets/df76829b-9a83-44bf-b16e-c450e1beb28f) <br><br>

3. When 'Test' is clicked, select 'Create new test event', Give an 'event name' & click 'Save'.

    ![image](https://github.com/user-attachments/assets/07bf9f52-7e52-4656-8b9e-eb411384bfe4)<br><br>

4. After creating the event, go to the 'IAM Console' and navigate to the 'Policies section' to 'create a new policy'. Select 'EC2' as the service and, in the Actions section, grant permissions for
   - DescribeInstances <br>
   - DescribeVolumes <br>
   - DescribeSnapshots <br>
   - DeleteSnapshots <br>

      ![image](https://github.com/user-attachments/assets/d81991a7-ff04-4d56-b28c-b8a01d412063) <br><br>

5. Give a 'Policy Name', and Click 'Create Policy'. <br>

    ![image](https://github.com/user-attachments/assets/2e34caaf-d783-41d1-8e98-7e9d47773254) <br><br>

6. Go to the 'Lambda function' page, select the newly created function, navigate to Configurations → Permissions, and click on the 'Role name'.

    ![image](https://github.com/user-attachments/assets/aaf49811-36a2-4e44-8ccc-d678aa435b99) <br><br>

7. Click on 'Add Permissions' and then select 'Attach Policy', select the correct policy, you just created. <br>

    ![image](https://github.com/user-attachments/assets/f6e9968a-3625-4ff6-ac13-b0e099a03b80) <br><br>

8. After that, you can go to the 'Lambda function' page and run the code; it will display some outputs as shown below. <br>

    ![image](https://github.com/user-attachments/assets/743e34d6-39da-439e-a2a3-2a906e285fa5) <br><br>

### Step 3 :
1. To test the 'Lambda function', navigate to the 'EC2 Console' and 'terminate' the EC2 instance.<br>
    ![image](https://github.com/user-attachments/assets/3ca8b1f4-8e89-4258-ae48-9daf3bb0a599) <br><br>
    
2. Go to the 'Lambda Console', navigate to the 'Lambda Function' page, and under the 'Code' section, click 'Test code' to run the function. It will display an output similar to the one shown below.<br>

    ![image](https://github.com/user-attachments/assets/1458ccc7-a550-40ce-bd30-514a1b9ee4fb) <br><br>

3. If the snapshot was linked to a missing volume, the Lambda function successfully deleted it. VOILA! 🎉

   ![image](https://github.com/user-attachments/assets/543ae245-2dd7-4491-a5f1-b85299bc0e2e)<br><br>


## 🔍 Architectural Insights:
Additionally, We can use 'Amazon CloudWatch' to automatically trigger the Lambda function at predefined intervals like every hour, day, minute, or second. However, this may result in **higher costs** because our Lambda execution time increases when triggered automatically. Nevertheless, manually triggering this function is a **better choice** because it allows us to trigger it when needed.

## CloudWatch/ EventBridge Implementation :
### Steps :
1. Navigate to CloudWatch Console, Go to 'Events'-> 'Rules'-> 'Create Rule'.<br>
2. Under 'Rule detail', give a 'name', 'description', 'Rule Type' = 'Schedule, click 'Continue in EventBridge Scheduler'.<br>
    ![image](https://github.com/user-attachments/assets/c32bece5-14ad-4ad5-b91c-ea4df2152431) <br><br>

3. Under 'Schedule Pattern', select 'Recurring schedule', 'Schedule Type'='Rate-based schedule' & 'Rate expression' = '1 hour' (We set for hourly)<br>
    ![image](https://github.com/user-attachments/assets/839e1529-40b4-4411-9272-a349702fce21) <br><br>

4. Select Target as 'Templated targets' -> 'AWS Lambda', select the lamdba functrion from dropdown, & 'Next'.<br>
    ![image](https://github.com/user-attachments/assets/cefbb4cf-8aae-4898-9cbb-ff8763b3111d)<br><br>

5. On the next page, choose 'None' for the 'Action after Schedule' option and 'Next'-> 'Review the details -> 'Create Schedule'.<br>
    ![image](https://github.com/user-attachments/assets/0c64095f-ca26-4eea-a6e6-bf1d559c5683)<br><br>

6. You have successfully created the CloudWatch scheduler, which will trigger the Lambda function every hour.However, please note that this setup will incur some costs since the function is triggered continuously every hour. Alternatively, we can configure it to run on specific days and times as needed.<br>

<h3> 🟢Happy Learning ! 🥁🙌🫶 </h3>
