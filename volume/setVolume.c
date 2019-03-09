#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <stdlib.h>
#include <linux/input.h>
#include <linux/soundcard.h>

#define MIXER_DEVICE "/dev/mixer"
#define CFG "config/volume.cfg"

int mixer = -1;

void daemonize(char *dir)
{
  if (fork() != 0)
    exit(0);
  setsid();
  if (fork() != 0)
    exit(0);
  chdir(dir);
  umask(0);
  close(0);
  close(1);
  close(2);
  /*STDIN*/
  open("/dev/null", O_RDONLY);
  /*STDOUT*/
  open("/dev/null", O_WRONLY);
  /*STDERR*/
  open("/dev/null", O_WRONLY);
}

void setVolume(int level)
{

  int oss_volume = level | (level << 8); // set volume for both channels

  if (ioctl(mixer, SOUND_MIXER_WRITE_VOLUME, &oss_volume) == -1)
  {
    fprintf(stderr, "Failed opening mixer for write - VOLUME\n");
  }
}

int getVolume()
{
  if (mixer == -1)
  {
    fprintf(stderr, "Key mixer not open\n");
    return -1;
  }

  int outvol = 0;
  if (ioctl(mixer, SOUND_MIXER_READ_VOLUME, &outvol))
  {
    fprintf(stderr, "Failed opening mixer for read - VOLUME\n");
    return -1;
  }
  return outvol & 0xff;
}

void writeCfg(int vol)
{
  FILE *fp; 
  fp=fopen(CFG, "w");

  if(fp == NULL)
    return;
  
  fprintf(fp, "%d\n", vol);
  fclose(fp);  
}

void increaseVol()
{
  int vol = getVolume();
  vol = vol + 10;

  if (vol > 255)
  {
    vol = 255;
  }

  writeCfg(vol);
  setVolume(vol);
}

void decreaseVol()
{
  int vol = getVolume();
  vol = vol - 10;
  if (vol < 0)
  {
    vol = 0;
  }

  writeCfg(vol);
  setVolume(vol);
}


void loadCfgVolume() 
{
  FILE* file = fopen (CFG, "r");
  if(file == NULL)
    return;

  int vol = 0;
  fscanf (file, "%d", &vol);
  printf("Loading volume from cfg: %d\n", vol); 
  setVolume(vol);
  fclose (file); 
}

int main(int argc, char* argv[])
{
  mixer = open(MIXER_DEVICE, O_WRONLY);

  int vol;
  if (argc == 2)
  {
    printf("New Volume is %s\n", argv[1]);
    vol = atoi(argv[1]);

    if (vol >= 255)
    {
      vol = 255;
    }

    if (vol < 0)
    {
      vol = 0;
    }

    setVolume(vol);
    writeCfg(vol);
    exit(0);
  }

  loadCfgVolume();

  char devname[] = "/dev/event0";
  int device = open(devname, O_RDONLY);
  struct input_event ev;

  //daemonize("/");

  while (1)
  {
    read(device, &ev, sizeof(ev));
    if (ev.type == 1 && ev.value == 1)
    {

      if (ev.code == 3)
      {
        increaseVol();
      }
      else if (ev.code == 2)
      {
        decreaseVol();
      }

      int vol = getVolume();
      //printf("Key: %i State: %i volume is %d\n", ev.code, ev.value, vol);
    }
  }
  close(mixer);
}
