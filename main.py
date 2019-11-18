from machine import Timer, PWM
import sensor
import lcd
import KPU as kpu


class Servo:
    def __init__(self,
                 pin,
                 freq,
                 min_duty,
                 max_duty,
                 timer,
                 channel,
                 initial_pos=0.5):
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.tim = Timer(timer, channel, mode=Timer.MODE_PWM)
        self._pos = initial_pos
        self.ch = PWM(
            self.tim,
            freq=freq,
            duty=self.position_to_duty(self._pos),
            pin=pin)

    def position_to_duty(self, pos):
        return (self.max_duty - self.min_duty) * pos + self.min_duty

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = min(max(pos, 0), 1)
        self.ch.duty(self.position_to_duty(self._pos))


def main():
    servo_freq = 50  # Hz

    servo_vert = Servo(
        pin=10,
        freq=servo_freq,
        min_duty=7,
        max_duty=11.5,
        timer=Timer.TIMER0,
        channel=Timer.CHANNEL0,
        initial_pos=0.5)

    servo_hor = Servo(
        pin=11,
        freq=servo_freq,
        min_duty=2.8,
        max_duty=11.5,
        timer=Timer.TIMER0,
        channel=Timer.CHANNEL1)

    lcd.init(freq=15000000)
    lcd.direction(lcd.YX_LRDU)
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_vflip(1)

    classes = [
        'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat',
        'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person',
        'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor'
    ]
    # target_class = 14  # person
    # target_class = 7  # cat
    target_class = 4  # bottle
    # target_class = 19  # monitor

    task = kpu.load(0x500000)

    anchor = (1.08, 1.19, 3.42, 4.41, 6.63, 11.38, 9.42, 5.11, 16.62, 10.52)
    a = kpu.init_yolo2(task, 0.05, 0.3, 5, anchor)

    sensor.run(1)

    while (True):
        img = sensor.snapshot()
        code = kpu.run_yolo2(task, img)
        if code:
            target_boxes = [d for d in code if d.classid() == target_class]
            if target_boxes:
                # change turret position
                target = max(target_boxes, key=lambda d: d.value())

                a = img.draw_rectangle(target.rect())
                a = lcd.display(img)
                for i in code:
                    lcd.draw_string(target.x(),
                                    target.y() + 12, '%f1.3' % target.value(),
                                    lcd.RED, lcd.WHITE)

                target_center_x = target.x() + target.w() // 2
                target_center_y = target.y() + target.h() // 2

                servo_hor.pos += 0.00005 * (
                    sensor.width() // 2 - target_center_x)
                servo_vert.pos -= 0.0005 * (
                    sensor.height() // 2 - target_center_y)

                # print('hor', servo_hor.pos)
                # print('vert', servo_vert.pos)
            else:
                a = lcd.display(img)
    kpu.deinit(task)


if __name__ == "__main__":
    main()
