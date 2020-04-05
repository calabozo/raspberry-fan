#include <syslog.h>
#include <unistd.h>
#include <stdio.h>
#include <wiringPi.h>


#define TEMP_INTERVAL_TIME 5
#define TEMP_STOP_FAN 56
#define TEMP_START_FAN 67
#define PIN  15

double get_temp(){
    FILE *temperatureFile;
    double temp;
    temperatureFile = fopen ("/sys/class/thermal/thermal_zone0/temp", "r");
    if (temperatureFile == NULL)
        return -1;
    fscanf (temperatureFile, "%lf", &temp);
    temp /= 1000;
    fclose (temperatureFile);
    return temp;
}

unsigned int call_stop_fan(){
    unsigned int fan_final_status=0;
    syslog(LOG_INFO,"Stopping fan");
    digitalWrite(PIN, LOW);
    return fan_final_status;
}

unsigned int call_start_fan(){
    unsigned int fan_final_status=1;
    syslog(LOG_INFO,"Starting fan");
    digitalWrite(PIN, HIGH);
    return fan_final_status;
}


int main(int argc, char *argv[]){
    double temp;
    double temp_start_fan=TEMP_START_FAN;
    double temp_stop_fan=TEMP_STOP_FAN;
    unsigned int fan_on;


    openlog("raspberry-fan", LOG_PID|LOG_CONS, LOG_USER);

    if (wiringPiSetup () == -1){
        syslog(LOG_ERR,"Cannot access GPIO");
	return 1;
    }
    pinMode (PIN, OUTPUT);

    fan_on=call_stop_fan();
    while(1){
        temp=get_temp();
        //syslog(LOG_DEBUG,"Temperature: %f",temp);
	if (fan_on && temp<=temp_stop_fan){
	    fan_on=call_stop_fan();
	}else if (!fan_on && temp>=temp_start_fan){
            fan_on=call_start_fan();
	}
        sleep(TEMP_INTERVAL_TIME);
    }
    closelog();
    return 0;
}
