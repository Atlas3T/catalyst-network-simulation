#include "unique_id_generator.h"

using simulation::unique_id_generator;

unique_id_generator * unique_id_generator::instance () {
   if (!only_copy) {
      only_copy = new unique_id_generator();
   }
   return only_copy;
}