
Bug 1:

Performing inferences on images...
Traceback (most recent call last):
  File "part2.py", line 13, in <module>
    BIM = cityBuilder.build()
  File "./BRAILS/brails/CityBuilder.py", line 247, in build
    story_df = storyModel.predict(self.BIM['StreetView'].tolist())
  File "./BRAILS/brails/modules/NumFloorDetector/NFloorDetector.py", line 264, in predict
    if overlapRatio[indKeep[k]]>10: stack4Address.append(indKeep[k])
IndexError: index 0 is out of bounds for axis 0 with size 0


I think this is because indKeep is empty.




Bug 2:
indKeep = np.argsort(-overlapRatio)[0:2]
IndexError: index 0 is out of bounds for axis 0 with size 0


The reason is: overlapRatio has less elements than you expected.



Bug 3:

 File "/scratch1/05735/c_w/projects/Laura/BRAILS/brails/modules/NumFloorDetector/lib/utils/utils.py", line 71, in <listcomp>
    normalized_imgs = [(img / 255 - mean) / std for img in ori_imgs]
TypeError: unsupported operand type(s) for /: 'NoneType' and 'int'