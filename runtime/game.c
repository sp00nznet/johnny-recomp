/* game.c - the facts about Johnny Castaway (SCRANTIC.SCR) that pcrecomp's Win16
 * host runtime needs. See <pcrecomp>/runtime/win16/host/recomp_game.h. */
#include "recomp_game.h"

const RecompGame recomp_game = {
    .title      = "Johnny Castaway",
    .guest_dir  = "C:\SIERRA\SCRANTIC",
    /* The installer writes [ScreenSaver.ScreenAntics] SourceDir to SCRANTIC.INI. */
    .ini_fallbacks = { "SCRANTIC.INI", NULL },
    .create_message = 1,
    .destroy_message = 1,
    .real_windows = 0,
    .real_clock = 1,
};
