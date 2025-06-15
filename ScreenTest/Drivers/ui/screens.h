#ifndef EEZ_LVGL_UI_SCREENS_H
#define EEZ_LVGL_UI_SCREENS_H

#include <lvgl.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct _objects_t {
    lv_obj_t *main;
    lv_obj_t *chart1;
    lv_obj_t *bpm_value;
    lv_obj_t *bpm_text;
    lv_obj_t *status;
    lv_obj_t *pr_label;
    lv_obj_t *qt_label;
    lv_obj_t *qrs_label;
    lv_obj_t *rr_segment_label;
    lv_obj_t *names;
    lv_obj_t *print_value;
    lv_obj_t *qt_int_value;
    lv_obj_t *qrs_com_value_2;
    lv_obj_t *rrseg_value_5;
    lv_obj_t *led;
} objects_t;

extern objects_t objects;

enum ScreensEnum {
    SCREEN_ID_MAIN = 1,
};

void create_screen_main();
void tick_screen_main();

void tick_screen_by_id(enum ScreensEnum screenId);
void tick_screen(int screen_index);

void create_screens();


#ifdef __cplusplus
}
#endif

#endif /*EEZ_LVGL_UI_SCREENS_H*/