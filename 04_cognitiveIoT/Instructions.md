# Instructions for execution
### Step 1 
1. Generate the QC(Quality check data) by running file color_kmeans.py in cmd
2. Enter the picture file name i.e 306
3. model number for referance i.e demo

The output will generate height & width along with the color detection using Kmeans algorithm. We have also used the microsoft vision for object detection, colour detection, bounding box dimenstion.

### Step 2 Chatbot and VoiceBot Created in Rasa Framework 

1. rasa train
2. rasa interactive  -m models/20190919-185625.tar.gz --endpoints endpoints.yml
3. rasa run --debug  --enable-api --log-file out.log -m models -p 5005 --connector socketio --credentials credentials.yml --endpoints endpoints.yml
4. python -m rasa_core_sdk.endpoint --actions action
5. rasa run actions --port 5057
6. docker run -p 8000:8000 rasa/duckling
7. rasa run --verbose --debug -m models -p 5007 --connector rest --credentials credentials.yml --endpoints endpoints.yml  --cors "*"  









