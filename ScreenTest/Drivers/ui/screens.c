#include <string.h>

#include "screens.h"
#include "images.h"
#include "fonts.h"
#include "actions.h"
#include "vars.h"
#include "styles.h"
#include "ui.h"

#include <string.h>

objects_t objects;
lv_obj_t *tick_value_change_obj;
uint32_t active_theme_index = 0;

void create_screen_main() {
    lv_obj_t *obj = lv_obj_create(0);
    objects.main = obj;
    lv_obj_set_pos(obj, 0, 0);
    lv_obj_set_size(obj, 480, 272);
    lv_obj_set_style_bg_color(obj, lv_color_hex(0xff000000), LV_PART_MAIN | LV_STATE_DEFAULT);
    {
        lv_obj_t *parent_obj = obj;
        {
            // chart1
            lv_obj_t *obj = lv_chart_create(parent_obj);
            objects.chart1 = obj;
            lv_obj_set_pos(obj, 11, 45);
            lv_obj_set_size(obj, 339, 147);
            lv_obj_set_style_bg_color(obj, lv_color_hex(0xff000000), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_border_opa(obj, 0, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_line_color(obj, lv_color_hex(0xff000000), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xffff0000), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_line_color(obj, lv_color_hex(0xffff0000), LV_PART_INDICATOR | LV_STATE_DEFAULT);
        }
        {
            // bpmValue
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.bpm_value = obj;
            lv_obj_set_pos(obj, 361, 15);
            lv_obj_set_size(obj, 73, 38);
            lv_obj_set_style_bg_grad_color(obj, lv_color_hex(0xff000000), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_line_color(obj, lv_color_hex(0xffeaeaea), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xffff0000), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_30, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_letter_space(obj, 2, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_align(obj, LV_TEXT_ALIGN_RIGHT, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text(obj, "000");
        }
        {
            // bpmText
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.bpm_text = obj;
            lv_obj_set_pos(obj, 434, 37);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xffff0000), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text(obj, "BPM");
        }
        {
            // Status
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.status = obj;
            lv_obj_set_pos(obj, 364, 221);
            lv_obj_set_size(obj, 70, 30);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xff50dd5e), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_align(obj, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text(obj, "Healthy");
        }
        {
            // PRLabel
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.pr_label = obj;
            lv_obj_set_pos(obj, 0, 201);
            lv_obj_set_size(obj, 130, 20);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xff12dde7), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_align(obj, LV_TEXT_ALIGN_RIGHT, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text(obj, "PR Interval");
        }
        {
            // QTLabel
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.qt_label = obj;
            lv_obj_set_pos(obj, 0, 221);
            lv_obj_set_size(obj, 130, 20);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xff12dde7), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_align(obj, LV_TEXT_ALIGN_RIGHT, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text(obj, "QT Interval");
        }
        {
            // PRSegmentLabel
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.pr_segment_label = obj;
            lv_obj_set_pos(obj, 205, 203);
            lv_obj_set_size(obj, 97, 20);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfffff000), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_align(obj, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text(obj, "PR Segment");
        }
        {
            // QRSLabel
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.qrs_label = obj;
            lv_obj_set_pos(obj, 0, 242);
            lv_obj_set_size(obj, 130, 20);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xff12dde7), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_align(obj, LV_TEXT_ALIGN_RIGHT, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text(obj, "QRS Complex");
        }
        {
            // STSegmentLabel
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.st_segment_label = obj;
            lv_obj_set_pos(obj, 205, 222);
            lv_obj_set_size(obj, 97, 20);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfffff000), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_align(obj, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text(obj, "ST Segment");
        }
        {
            // Names
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.names = obj;
            lv_obj_set_pos(obj, 376, 160);
            lv_obj_set_size(obj, 92, 32);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xffffffff), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_10, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_align(obj, LV_TEXT_ALIGN_RIGHT, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text(obj, "Tunahan Kaya\n\nBugra Alp Aydin");
        }
        {
            // PRintValue
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.print_value = obj;
            lv_obj_set_pos(obj, 141, 203);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xffffffff), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text(obj, "000ms");
        }
        {
            // QTIntValue
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.qt_int_value = obj;
            lv_obj_set_pos(obj, 141, 224);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xffffffff), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text(obj, "000ms");
        }
        {
            // QRSComValue_2
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.qrs_com_value_2 = obj;
            lv_obj_set_pos(obj, 141, 244);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xffffffff), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text(obj, "000ms");
        }
        {
            // prsegValue_3
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.prseg_value_3 = obj;
            lv_obj_set_pos(obj, 302, 204);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xffffffff), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text(obj, "000ms");
        }
        {
            // stsegValue_4
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.stseg_value_4 = obj;
            lv_obj_set_pos(obj, 303, 223);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xffffffff), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text(obj, "000ms");
        }
        {
            lv_obj_t *obj = lv_led_create(parent_obj);
            objects.obj0 = obj;
            lv_obj_set_pos(obj, 436, 216);
            lv_obj_set_size(obj, 32, 32);
            lv_led_set_color(obj, lv_color_hex(0xff00ff03));
            lv_led_set_brightness(obj, 255);
        }
    }
    
    tick_screen_main();
}

void tick_screen_main() {
}



typedef void (*tick_screen_func_t)();
tick_screen_func_t tick_screen_funcs[] = {
    tick_screen_main,
};
void tick_screen(int screen_index) {
    tick_screen_funcs[screen_index]();
}
void tick_screen_by_id(enum ScreensEnum screenId) {
    tick_screen_funcs[screenId - 1]();
}

void create_screens() {
    lv_disp_t *dispp = lv_disp_get_default();
    lv_theme_t *theme = lv_theme_default_init(dispp, lv_palette_main(LV_PALETTE_BLUE), lv_palette_main(LV_PALETTE_RED), false, LV_FONT_DEFAULT);
    lv_disp_set_theme(dispp, theme);
    
    create_screen_main();
}
