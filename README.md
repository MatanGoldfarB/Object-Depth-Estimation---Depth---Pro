## Integrating Apple Depth Pro with yolov11 for object depth estimation
# Expirementing with the model to see its precision

to run it by yourself pull from apple-depth-pro github: https://github.com/apple/ml-depth-pro.git

then add in the folder ml-depth-pro depth_test and only change the file for the test.

# My Expirement
- When the image is small, the model performs significantly worse, which makes sense since we focus on pixel-level differences.
- The model can run on GPU, but there’s no noticeable speed improvement.
- In practice, the model can be used to generate a dataset, so speed is less critical.
- A key insight is that the depth value provided by the model corresponds to the pixel at the center of the object. In our case, we took the center of the bounding box.
- Each run takes about 5–8 minutes.
- If we want to understand why the model sometimes underperforms, it’s also worth testing with cameras that are not iPhones (to avoid relying on a fixed focal length, which iPhones do not reveal).
- Tried to trick it with zoom and it did not preform well.
- Some new models are emerging with much better performance and are very relevant to our work.
- We should add focal length explicitly when available, especially when we input it manually and not rely on EXIF metadata.

| Scene # | Distance [m] | Model Output [m] | Absolute Error [m] | Accuracy [%] |
|--------:|--------------:|------------------:|---------------------:|---------------:|
| 1       | 0.2           | 0.27              | 0.07                 | 35%            |
| 2       | 0.5           | 0.69              | 0.19                 | 38%            |
| 3       | 1             | 1.11              | 0.11                 | 11%            |
| 4       | 2             | 2.11              | 0.11                 | 5.5%           |
| 5       | 0.2           | 0.30              | 0.10                 | 50%            |
| 6       | 0.5           | 0.52              | 0.02                 | 4%             |
| 7       | 1             | 0.92              | 0.08                 | 8%             |
| 8       | 2             | 1.86              | 0.14                 | 7%             |
| 9       | 3             | 2.74              | 0.26                 | 8.6%           |
| 10      | 4             | 3.42              | 0.58                 | 14.5%          |
