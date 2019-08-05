// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME srcdIRGS_dict

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "RConfig.h"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// Since CINT ignores the std namespace, we need to do so in this file.
namespace std {} using namespace std;

// Header files passed as explicit arguments
#include "include/RGS.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static TClass *RGS_Dictionary();
   static void RGS_TClassManip(TClass*);
   static void *new_RGS(void *p = 0);
   static void *newArray_RGS(Long_t size, void *p);
   static void delete_RGS(void *p);
   static void deleteArray_RGS(void *p);
   static void destruct_RGS(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::RGS*)
   {
      ::RGS *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::RGS));
      static ::ROOT::TGenericClassInfo 
         instance("RGS", "RGS.h", 73,
                  typeid(::RGS), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &RGS_Dictionary, isa_proxy, 0,
                  sizeof(::RGS) );
      instance.SetNew(&new_RGS);
      instance.SetNewArray(&newArray_RGS);
      instance.SetDelete(&delete_RGS);
      instance.SetDeleteArray(&deleteArray_RGS);
      instance.SetDestructor(&destruct_RGS);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::RGS*)
   {
      return GenerateInitInstanceLocal((::RGS*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::RGS*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *RGS_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::RGS*)0x0)->GetClass();
      RGS_TClassManip(theClass);
   return theClass;
   }

   static void RGS_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_RGS(void *p) {
      return  p ? new(p) ::RGS : new ::RGS;
   }
   static void *newArray_RGS(Long_t nElements, void *p) {
      return p ? new(p) ::RGS[nElements] : new ::RGS[nElements];
   }
   // Wrapper around operator delete
   static void delete_RGS(void *p) {
      delete ((::RGS*)p);
   }
   static void deleteArray_RGS(void *p) {
      delete [] ((::RGS*)p);
   }
   static void destruct_RGS(void *p) {
      typedef ::RGS current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::RGS

namespace {
  void TriggerDictionaryInitialization_RGS_dict_Impl() {
    static const char* headers[] = {
"include/RGS.h",
0
    };
    static const char* includePaths[] = {
"/cvmfs/sft.cern.ch/lcg/releases/ROOT/6.16.00-42022/x86_64-centos7-gcc8-opt/include",
"/afs/cern.ch/user/p/pmoder/RGS/",
0
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "RGS_dict dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
class __attribute__((annotate("$clingAutoload$include/RGS.h")))  RGS;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "RGS_dict dictionary payload"

#ifndef G__VECTOR_HAS_CLASS_ITERATOR
  #define G__VECTOR_HAS_CLASS_ITERATOR 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H
#include "include/RGS.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[]={
"RGS", payloadCode, "@",
nullptr};

    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("RGS_dict",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_RGS_dict_Impl, {}, classesHeaders, /*has no C++ module*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_RGS_dict_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_RGS_dict() {
  TriggerDictionaryInitialization_RGS_dict_Impl();
}
