"""
Alunos:
    Matheus Teixeirense da Silva Arcanjo   RA:22221020-5
"""

from controller import Robot, Supervisor, LED

TIME_STEP = 30
MAX_SPEED = 6.00
WAIT_TIME = 64.0

def iniciar(robot, supervisor):
    leftMotor = robot.getDevice("left wheel motor")
    rightMotor = robot.getDevice("right wheel motor")
    leftMotor.setPosition(float('inf'))
    rightMotor.setPosition(float('inf'))
    leftMotor.setVelocity(0.0)
    rightMotor.setVelocity(0.0)
    
    caixa = supervisor.getFromDef("caixaLeve")
    
    proximitySensors = [robot.getDevice(f"ps{i}") for i in range(8)]
    for sensor in proximitySensors:
        sensor.enable(TIME_STEP)
    
    leds = [robot.getDevice(f"led{i}") for i in range(10)]
    for led in leds:
        led.set(0)
        
    timer = 0.0
    lock = False
    foundBox = False
    caixaInit = None

    while robot.step(TIME_STEP) != -1:
        timer += 1.0
        caixaPos = caixa.getPosition()
        
        if timer == WAIT_TIME:
            caixaInit = caixa.getPosition()
            lock = True
            print("Nao")
                
        if lock:
            if caixaInit != caixaPos:
                foundBox = True
        
        if foundBox:
            leftTurn = 0.0
            rightTurn = 0.0
            leftMotor.setVelocity(0.0)
            rightMotor.setVelocity(0.0)
    
            for led in leds:
                led.set(1)
    
            print('CAIXA ENCONTRADA!!!')
            break

        leftTurn = MAX_SPEED / 1.50
        rightTurn = MAX_SPEED / 1.50
        
        rightSensorActive = False
        leftSensorActive = False
    
        for i in range(4):
            if proximitySensors[i].getValue() > 100:
                rightSensorActive = True
                leftTurn = 0.20 * MAX_SPEED
                rightTurn = MAX_SPEED
                break
                
        for i in range(4, 8):
            if proximitySensors[i].getValue() > 100:
                leftSensorActive = True
                leftTurn = MAX_SPEED
                rightTurn = 0.20 * MAX_SPEED
                break
                
        if rightSensorActive and leftSensorActive:
            leftTurn = -MAX_SPEED
            rightTurn = MAX_SPEED

        leftMotor.setVelocity(leftTurn)
        rightMotor.setVelocity(rightTurn)
        pass

if __name__ == "__main__":
    robot = Robot()
    supervisor = Supervisor() 
    iniciar(robot, supervisor)