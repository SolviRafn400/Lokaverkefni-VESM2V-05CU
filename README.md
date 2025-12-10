# Lokaverkefni-VESM2V-05CU
## íhlutir
* RasberryPi 5
* esp32-s3
* DFPlayer
* speakers
* 2 servo móters
* laser diode
* neopixel ring ljós

## Mótor laser
<img width="595" height="794" alt="image" src="https://github.com/user-attachments/assets/fc385095-db86-4749-8ee2-2a86e930f749" />

* 2 Micro Servo Motors (MG90S)
* 1 Laser diode
* Source. (*alliexpress link hérna*)
  
  hugmyndin var að mappa moteranna við myndavél þannig það getur beinið laser á fólk via facial recognition.

## Myndavél
<img width="595" height="794" alt="image" src="https://github.com/user-attachments/assets/25d5a068-786b-4282-a82c-710845b60dc3" />

* Picameras V3

  við erum að nota rasberry Py camera V3 handa facial recognition að nota (*general info hér*)

## audio speakers
<img width="595" height="794" alt="image" src="https://github.com/user-attachments/assets/7207a108-b186-449b-be15-43de385ec7d4" />

* DFPlayer
* Stereo Enclosed Speaker Set
* 1GB SDCard

  við notum DFPlayer með SDCard sem heldur við nokkur sound files af portal turret sem við fundum hér(https://tuna.voicemod.net/search/sounds/portal-turret/).
  við erum svo með tvo sterio hátalara sem ef er of stórt handa 3D Printið þá notum við minni hátalara

## 3D print
<img width="595" height="794" alt="image" src="https://github.com/user-attachments/assets/b7ac0088-49bd-49bb-a1fb-d9d7bcb71b20" />

* (*insert link or something here*)
* tinkercad
* blender
* svart acrylic málingu

  við notuðum tinkercad handa 3d modelið hjá armana, tannhjólinn og fæturnar. En handa aðal búkinn þurftu við að nota blender því 3D modelið var of flókið handa tinkercad. svo þegar við vorum comin með #d printið þá máluðum við það með svörtum acrylic málingu.
  (*meiri info hér ef hægt*)

## RasberryPi
<img width="595" height="794" alt="image" src="https://github.com/user-attachments/assets/12029638-cd14-4325-9130-a3f1bd5bb697" />

* RasberryPi 5

  við erum að nota RasberryPi 5 til að halda aðal codeið. hann er téingdur við myndavélinna til að geta leifa facial recognition codið að nota, hann er teingdur við ESP32ið til að tala við móteranna og dfplayeranna.

## Sketch hugmynd
![IMG_3727](https://github.com/user-attachments/assets/466e7b5c-e6ab-4a20-bcbf-fc4b43e28062)

hugmyndin var að búa til turret frá leiknum Portal 2. okkur lángaði að það gæti miðað á fólk með laser og ítt armanna út þegar myndavélinn sá einhvern og látið ljós blikka í armana eins og hann var að skjóta þig. svo lánguðum við að geta teingið við myndavélinna frá símannum með niceguy. 

en út af of littlum tíma og tæknilega erfileika þurftu við að yfirgefa niceguy og ljósin í armanna og og að hafa mótor til að ýta armana út og focusa á facial recognition, laser móteranna og audioið.
