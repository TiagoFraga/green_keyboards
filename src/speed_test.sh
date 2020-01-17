#!/bin/bash



text_input(){
	adb shell input text "b"
	adb shell input text "a"
	adb shell input text "t"
	adb shell input text "a"
	adb shell input text "t"
	adb shell input text "a"
	adb shell input text "\ "
	adb shell input text "b"
	adb shell input text "a"
	adb shell input text "t"
	adb shell input text "a"
	adb shell input text "t"
	adb shell input text "a"
	adb shell input text "\ "
	adb shell input text "b"
	adb shell input text "a"
	adb shell input text "t"
	adb shell input text "a"
	adb shell input text "t"
	adb shell input text "a"
}

text_input_full_write_word(){
	adb shell "input text 'b' && input text 'a'  &&  input text 't' &&  input text 'a'  && input text 't'  && input text 'a'"
	adb shell input text '\ '
	adb shell "input text 'b' && input text 'a'  &&  input text 't' &&  input text 'a'  && input text 't'  && input text 'a'"
	adb shell input text '\ '
	adb shell "input text 'b' && input text 'a'  &&  input text 't' &&  input text 'a'  && input text 't'  && input text 'a'"
	
}




tap_input(){
	adb shell input tap 640 1540 #  b
	adb shell input tap 100 1400 #  a
	adb shell input tap 466 1247 #  t
	adb shell input tap 100 1400 #  a
	adb shell input tap 466 1247 #  t
	adb shell input tap 100 1400 #  a
	adb shell input tap 363 1715 #  space
	adb shell input tap 640 1540 #  b
	adb shell input tap 100 1400 #  a
	adb shell input tap 466 1247 #  t
	adb shell input tap 100 1400 #  a
	adb shell input tap 466 1247 #  t
	adb shell input tap 100 1400 #  a
	adb shell input tap 363 1715 #  space
	adb shell input tap 640 1540 #  b
	adb shell input tap 100 1400 #  a
	adb shell input tap 466 1247 #  t
	adb shell input tap 100 1400 #  a
	adb shell input tap 466 1247 #  t
	adb shell input tap 100 1400 #  a

}


swipe_input(){
	adb shell input swipe 640 1540 640 1540 0 #  b
	adb shell input swipe 100 1400 100 1400 0 #  a
	adb shell input swipe 466 1247 466 1247 0 #  t
	adb shell input swipe 100 1400 100 1400 0 #  a
	adb shell input swipe 466 1247 466 1247 0 #  t
	adb shell input swipe 100 1400 100 1400 0 #  a
	adb shell input swipe 363 1715 363 1715 0 #  space
	adb shell input swipe 640 1540 640 1540 0 #  b
	adb shell input swipe 100 1400 100 1400 0 #  a
	adb shell input swipe 466 1247 466 1247 0 #  t
	adb shell input swipe 100 1400 100 1400 0 #  a
	adb shell input swipe 466 1247 466 1247 0 #  t
	adb shell input swipe 100 1400 100 1400 0 #  a
	adb shell input swipe 363 1715 363 1715 0 #  space
	adb shell input swipe 640 1540 640 1540 0 #  b
	adb shell input swipe 100 1400 100 1400 0 #  a
	adb shell input swipe 466 1247 466 1247 0 #  t
	adb shell input swipe 100 1400 100 1400 0 #  a
	adb shell input swipe 466 1247 466 1247 0 #  t
	adb shell input swipe 100 1400 100 1400 0 #  as

}


start=$(python -c 'import time; print(str(int(round(time.time() * 1000)))) ')
text_input
end=$(python -c 'import time; print(str(int(round(time.time() * 1000)))) ')
runtime=$(python -c "print(str($end - $start))")
echo "Input Text elapsed time: $runtime ms"
#######################
adb shell input text "\ "
start=$(python -c 'import time; print(str(int(round(time.time() * 1000)))) ')
text_input_full_write_word
end=$(python -c 'import time; print(str(int(round(time.time() * 1000)))) ')
runtime=$(python -c "print(str($end - $start))")
echo "Input Text full write elapsed time: $runtime ms"
#######################
adb shell input text "\ "
start=$(python -c 'import time; print(str(int(round(time.time() * 1000)))) ')
tap_input
end=$(python -c 'import time; print(str(int(round(time.time() * 1000)))) ')
runtime=$(python -c "print(str($end - $start))")
echo "Input Tap elapsed time: $runtime ms"
########################
adb shell input text "\ "
start=$(python -c 'import time; print(str(int(round(time.time() * 1000)))) ')
swipe_input
end=$(python -c 'import time; print(str(int(round(time.time() * 1000)))) ')
runtime=$(python -c "print(str($end - $start))")
echo "Input Swipe elapsed time: $runtime ms"



