# Guide how to build your own secure pico box

This guide is from start to finish how i went about building the box and some the issues i came across as well as helpful tips. Professionally i am landscape gardener so building side was easyish but i did do a couple mistakes along the process building as its something i have never done.

![Front view](IMG_20250123_120316757.jpg)

![Top view](IMG_20250123_120321885.jpg)

![Inside view](IMG_20250123_120335198.jpg)

![Layout](layout.jpg)

## Step 1 Building the frames
![The frames](build_the_frames.jpg) 
At this stage you will need to build two frame exactly the same size as these will be used to build the main box. You will also need a third frame for the lid (top). At this point you must decide if your going to partition the box so that you have multiple lids and bays if your likely to have multiple deliverys a day. This will also need more drop bolt locks and door sensors as well as more coding.

## Step 2 Install frames together
![Installing frames together](install_frames_together.jpg)
This stage is connecting the frames together so that they form a box. As you may notice the third frame is for the lid.

## Step 3 Install flooring support
![Install flooring support](install_flooring_support.jpg)
During this stage you will need to attach some smaller lengths and thickness of wood and add to the inside of the bottom frame so that you can screw or nail down in my case tongue and groove boards.

## Step 4 nailing tongue and groove boards.
![Nailing tongue and groove boards](install_flooring.jpg)
Title self explanatory i used tongue and groove boards as i built this box from spares but you can use plywood board or some other type of board thats somewhat waterproof/splashproof.

## Step 5 Install cladding
![Install cladding](install_cladding.jpg)
VERY IMPORTANT! While i have put the cladding on vertically as my box is under a porch if you decide to use featheredge boards make sure they are put on HORIZONTAL starting from bottom working your way up. Reason for this is driving rain can get through into the box if you live in country with alot rain like i do (uk). Also dont clad the back of the box until you install hidges and top!.Their is a massive amount cladding options out their from tongue and grove boards to composite cladding etc.

Make sure if you go down a wooden route you use ring shank nails as wood when it gets wet expands and contracts. which if you use non ring shank nails will make the boards pop off / loose over time. Its also not adviseable to use screws as it makes it easier to access the box.

## Step 6 Install hinges
![Install Hinges](install_hinges.jpg)
This is the point you install the hinges and top and if you were like me and got carried away cladding the whole box your have to take back of the cladding off!!! WASNT EASY not the way i cladded it on!.

## Step 7 Finish the cladding
![Finish cladding](finish_cladding.jpg)
This is where you finish the cladding off on the back making sure to cover up the hidge screws on bottom section of the hidge but also making sure its not too high that it stops your lid opening. Remeber we dont want the top to open to far back so if delievery driver leaves it open it doesnt spring back shut. I used standard door hindges for this.

## Step 8 Cladding top and paint
![Cladding top and paint](cladding_top.jpg)
For the top i used once again tongue and groove boards then i went round the edges cladding so that the felt has got nice smooth area to nail to but also to cover up the screws on top part hindges. During this stage you can use any type board mdf or plywood sheets as this section will be felted.

## Step 9 Cutting the felt
![Cutting the felt](felt.jpg)
Measure felt out so that it covers the top as well as the side cladding.

## Step 10 Nailing felt and folding
![Folding felt](folding.jpg)

![Nailing](folding_2.jpg)

This stage can be tricky to do if weather is cold like it was in uk when i did this. Felt isnt very bendy during cold temperatures and is likely to rip when folding hence why i brought this inside. Make sure you keep the felt taught as possible to reduce bubbling. Bubbling your see on second picture front but it doesnt matter to much around sides as we will clad these again which will cover them up plus the folds.

## Step 11 Installing Electric Drop Bolt Lock 12v
![Installing drop bolt lock](picobox2.jpg)

This stage can be tricky depending on type lock you get. I got electric drop bolt lock 12v from amazon which came in two parts [Amazon link](https://www.amazon.co.uk/LIBO-Electric-Electronic-Control-Security/dp/B07DW17J3Q/ref=sr_1_3?crid=3IMLO5TY7DW8C&dib=eyJ2IjoiMSJ9.hp2-itwyPUYHBJkAGXtzGxl7cBORglDBRUbYQpckPmc9WOuCHS1eXhC6ao8Yo6jCnItKoFeXaxsLDI9x0FOoczluv7sMgIcYGWtJ3Rzg98wND53W8JTD2CmEj2bEbKm1wl87hja0fNYtyToEtqWZSImI0eUMZtIWXg78s6UZm0SwW9PhYKXOubZoEPymGDgl2R3VeDV7jQN-EwN_8hxK6gqQQD8cuNf6WY_5Svq2c-ml-kG4rfwiejUSuTVRsCRkVPt7G3zcD3Eg0r-zuU_sxQHwqYaZiab0ZEOYoB-1H33oisJFurZfUgSz7PWrY2VXm-xuJ9r13BwGC7LCZtCJ5Q-tbDGtYkTdPOawtP_ydbUOnxM0t7EHgJyOKrLL1HeH2t3r9AjHXSWdzG3ewiGYn5-CPKJAPxeEOVc4tHjU0SD-H-a1pew6RCmiIraZKoqn.DI0taTb2DdbJ4WJ4xTMYhRsks2dMf-DbFepCZLddo_4&dib_tag=se&keywords=Electronic+dropbolt+lock+12v&qid=1737649583&sprefix=electronic+dropbolt+lock+12v%2Caps%2C76&sr=8-3). I installed an extra piece wood so electronic part of lock is set back and screwed on.

![Installing drop bolt lock part 2](plate_for_lock.jpg)
I took the second part of the lock apart to use the plate because the lock doesnt work without the magnet in place. I screwed this on to box and drilled out the hole so the drop bolt can extend into the frame.

![Installing drop bolt lock part 3](dropboltlock3.jpg)
Iv tested this lock its insanely strong. Also note it comes with 4 wires but in instructions only power works so yellow and white wire are redundant.

## Step 12 Test your setup
![Test your setup](test_setup.jpg)
Test you setup before installing amount errors i found with hardware for instance bme280 sensor i orginally had this in a breadboard and wouldnt work kept getting eio errors yet wired directly fine so worth testing before you install in box. It's also worth testing out the vibration sensor because mine wasn't sensitive enough so by adjusted the screw on the sensor I found the sweet spot.

## Step 13 Install pico and sensors
![Install pico and sensors](picobox.jpg)
This is the stage you install waterproof boxs and install pico and sensors around the box. I installed bulk mine in the lid because its less wires interfering with moving parts as well leaves more room in bottom box for parcels. I decided to use 12v battery because orginally i was going to solar panel the top but the way uk is for sunshine in winter it wouldnt really work. You can also use mains supply using something like a 12v powersupply something i might end up doing once i see how long this 12v 5ah battery lasts. Still testing as i write this.

The drop bolt lock and siren work from 12v supply and using the relays to control these circuits. Make sure you wire these circuits up so that 1. If you pico loses power it releases the drop bolt lock 2. If your pico loses power siren activates. Getting these wrong could leave you with a locked box and no way in!

Powering the pico i got 12v to 5v dc to dc converter which is on its own circuit to 12v battery.

![Layout](layout.jpg)
Here is layout. This stage you can also do finishing touches like installing a handle setting up soft close lid hinge to reduce slamming/shaking, lid ratting, lose wires. having the soft close lid hinge also stops them opening the box right up or leaning it against a wall not closing.
