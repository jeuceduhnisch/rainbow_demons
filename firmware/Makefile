# Rainbow Demons - root project Makefile
#
# Build and flash from this final-release firmware folder.
# Assumes the standard DaisyExamples layout, where libDaisy and DaisySP sit two
# folders up, as siblings of patch_sm:
#   DaisyExamples/
#     libDaisy/
#     DaisySP/
#     patch_sm/
#       RAINBOW_DEMONS_WORKING_RELEASE/firmware/  <- this folder
#
# Usage from Git Bash, run from this folder:
#   make clean
#   make
#   make program-dfu
#
# If your libDaisy/DaisySP checkout lives somewhere else, override on the
# command line instead of editing this file, e.g.:
#   make LIBDAISY_DIR=/c/path/to/libDaisy DAISYSP_DIR=/c/path/to/DaisySP
# Prefer a normal DaisyExamples checkout when present. On this workstation the
# known-good SDK is kept in Documents/Codex, so fall back to that automatically.
# An explicit command-line override still wins, for example:
#   make LIBDAISY_DIR=/c/other/libDaisy DAISYSP_DIR=/c/other/DaisySP
LOCAL_LIBDAISY := ../../libDaisy
LOCAL_DAISYSP  := ../../DaisySP
# Use C:/ form here. Windows make.exe invokes arm-none-eabi-g++ directly, so an
# embedded /c/... path is not passed through Git Bash's path converter.
WORKING_SDK_ROOT := C:/Users/Jeuce/Documents/Codex/2026-07-07/i-h/work

LOCAL_LIBDAISY_READY := $(and \
	$(wildcard $(LOCAL_LIBDAISY)/src/daisy_patch_sm.h),\
	$(wildcard $(LOCAL_LIBDAISY)/Drivers/CMSIS_5/CMSIS/Core/Include/cmsis_gcc.h),\
	$(wildcard $(LOCAL_LIBDAISY)/build/libdaisy.a))

LIBDAISY_DIR ?= $(if $(LOCAL_LIBDAISY_READY),$(LOCAL_LIBDAISY),$(WORKING_SDK_ROOT)/libDaisy)
LOCAL_DAISYSP_READY := $(and \
	$(wildcard $(LOCAL_DAISYSP)/Source/daisysp.h),\
	$(wildcard $(LOCAL_DAISYSP)/build/libdaisysp.a))
DAISYSP_DIR  ?= $(if $(LOCAL_DAISYSP_READY),$(LOCAL_DAISYSP),$(WORKING_SDK_ROOT)/DaisySP)

TARGET := RainbowDemons
BUILD_DIR := build
USBPID := df11
FLASH_ADDRESS ?= 0x08000000
INTERNAL_ADDRESS := 0x08000000

CC := arm-none-eabi-gcc
CXX := arm-none-eabi-g++
AS := arm-none-eabi-gcc -x assembler-with-cpp
CP := arm-none-eabi-objcopy
SZ := arm-none-eabi-size

CPU = -mcpu=cortex-m7
FPU = -mfpu=fpv5-d16
FLOAT-ABI = -mfloat-abi=hard
MCU = $(CPU) -mthumb $(FPU) $(FLOAT-ABI)

OPT ?= -O2

CPP_SOURCES := RainbowDemons.cpp
C_SOURCES := startup_stm32h750xx.c
FATFS_DIR := $(LIBDAISY_DIR)/Middlewares/Third_Party/FatFs/src

C_DEFS := \
	-DUSE_HAL_DRIVER \
	-DSTM32H750xx \
	-DHSE_VALUE=16000000 \
	-DCORE_CM7 \
	-DSTM32H750IB \
	-DARM_MATH_CM7 \
	-DUSE_FULL_LL_DRIVER \
	-DFILEIO_ENABLE_FATFS_READER

C_INCLUDES := \
	-I. \
	-I$(LIBDAISY_DIR) \
	-I$(LIBDAISY_DIR)/src \
	-I$(LIBDAISY_DIR)/src/sys \
	-I$(LIBDAISY_DIR)/src/usbd \
	-I$(LIBDAISY_DIR)/src/usbh \
	-I$(LIBDAISY_DIR)/Drivers/CMSIS_5/CMSIS/Core/Include \
	-I$(LIBDAISY_DIR)/Drivers/CMSIS-DSP/Include \
	-I$(LIBDAISY_DIR)/Drivers/CMSIS-Device/ST/STM32H7xx/Include \
	-I$(LIBDAISY_DIR)/Drivers/STM32H7xx_HAL_Driver/Inc \
	-I$(LIBDAISY_DIR)/Middlewares/ST/STM32_USB_Device_Library/Core/Inc \
	-I$(LIBDAISY_DIR)/Middlewares/ST/STM32_USB_Host_Library/Core/Inc \
	-I$(LIBDAISY_DIR)/Middlewares/ST/STM32_USB_Host_Library/Class/MSC/Inc \
	-I$(LIBDAISY_DIR)/Middlewares/ST/STM32_USB_Host_Library/Class/MIDI/Inc \
	-I$(FATFS_DIR) \
	-I$(DAISYSP_DIR)/Source

CPPFLAGS := $(MCU) $(C_DEFS) $(C_INCLUDES) $(OPT) -Wall -Wextra -Wno-psabi -Wno-stringop-overflow -fdata-sections -ffunction-sections -fno-exceptions -fno-rtti -fshort-enums -g -ggdb
CFLAGS := $(MCU) $(C_DEFS) $(C_INCLUDES) $(OPT) -Wall -Wextra -Wno-psabi -Wno-stringop-overflow -fdata-sections -ffunction-sections -g -ggdb -MMD -MP
ASFLAGS := $(MCU) $(C_DEFS) $(C_INCLUDES) $(OPT) -Wall -fdata-sections -ffunction-sections

LDSCRIPT := $(LIBDAISY_DIR)/core/STM32H750IB_flash.lds
LDFLAGS := $(MCU) --specs=nano.specs --specs=nosys.specs -T$(LDSCRIPT) \
	-L$(LIBDAISY_DIR)/build -L$(DAISYSP_DIR)/build \
	-ldaisy -ldaisysp -lc -lm -lnosys \
	-Wl,-Map=$(BUILD_DIR)/$(TARGET).map,--cref -Wl,--gc-sections -Wl,--print-memory-usage

TARGET_BIN := $(TARGET).bin
TARGET_ELF := $(TARGET).elf

OBJECTS := $(BUILD_DIR)/startup_stm32h750xx.o $(BUILD_DIR)/$(TARGET).o

.PHONY: all clean size program-dfu program diagnostic-no-sdram-write program-dfu-no-sdram-write openocd checksdk

all: checksdk $(BUILD_DIR)/$(TARGET).elf $(BUILD_DIR)/$(TARGET).bin

# Fails fast with a clear message instead of a confusing compiler error if the
# SDK paths above don't actually point at a built libDaisy/DaisySP checkout.
checksdk:
	@test -f $(LIBDAISY_DIR)/src/daisy_patch_sm.h || (echo "ERROR: daisy_patch_sm.h not found under LIBDAISY_DIR=$(LIBDAISY_DIR). Check the path or override it: make LIBDAISY_DIR=/path/to/libDaisy" && exit 1)
	@test -f $(LIBDAISY_DIR)/Drivers/CMSIS_5/CMSIS/Core/Include/cmsis_gcc.h || (echo "ERROR: cmsis_gcc.h missing under $(LIBDAISY_DIR)/Drivers/CMSIS_5/CMSIS/Core/Include - check LIBDAISY_DIR or initialize the libDaisy submodules" && exit 1)
	@test -f $(LIBDAISY_DIR)/build/libdaisy.a || (echo "ERROR: libdaisy.a not found under $(LIBDAISY_DIR)/build - libDaisy itself hasn't been built yet. Run: (cd $(LIBDAISY_DIR) && make)" && exit 1)
	@test -f $(DAISYSP_DIR)/build/libdaisysp.a || (echo "ERROR: libdaisysp.a not found under $(DAISYSP_DIR)/build - DaisySP itself hasn't been built yet. Run: (cd $(DAISYSP_DIR) && make)" && exit 1)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/startup_stm32h750xx.o: $(C_SOURCES) Makefile | $(BUILD_DIR)
	$(CC) -c $(CFLAGS) -std=gnu11 -Wa,-a,-ad,-alms=$(BUILD_DIR)/startup_stm32h750xx.lst $< -o $@

$(BUILD_DIR)/$(TARGET).o: $(CPP_SOURCES) Makefile | $(BUILD_DIR)
	$(CXX) -c $(CPPFLAGS) -std=gnu++14 -Wa,-a,-ad,-alms=$(BUILD_DIR)/$(TARGET).lst $< -o $@

$(BUILD_DIR)/$(TARGET).elf: $(OBJECTS) Makefile
	$(CXX) $(OBJECTS) $(LDFLAGS) -o $@

$(BUILD_DIR)/$(TARGET).bin: $(BUILD_DIR)/$(TARGET).elf | $(BUILD_DIR)
	$(CP) -O binary -S $< $@

size: $(BUILD_DIR)/$(TARGET).elf
	$(SZ) $<

program-dfu: all
	dfu-util -a 0 -s $(FLASH_ADDRESS):leave -D $(BUILD_DIR)/$(TARGET).bin -d ,0483:$(USBPID)

program: program-dfu

# Diagnostic only: capture timing and monitoring remain active, but Mode 2/3
# do not write samples to external SDRAM. This intentionally does not produce
# a usable recording; it isolates SDRAM-write coupling into the audio input.
diagnostic-no-sdram-write:
	"$(MAKE)" clean
	"$(MAKE)" CPPFLAGS="$(CPPFLAGS) -DRAINBOW_DEMONS_DIAGNOSTIC_NO_SDRAM_WRITE"

program-dfu-no-sdram-write: diagnostic-no-sdram-write
	dfu-util -a 0 -s $(FLASH_ADDRESS):leave -D $(BUILD_DIR)/$(TARGET).bin -d ,0483:$(USBPID)

openocd:
	openocd -f interface/stlink.cfg -f target/stm32h7x.cfg

clean:
	rm -rf $(BUILD_DIR)

-include $(wildcard $(BUILD_DIR)/*.d)
