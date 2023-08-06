/* *********************************************************************
 * This Original Work is copyright of 51 Degrees Mobile Experts Limited.
 * Copyright 2019 51 Degrees Mobile Experts Limited, 5 Charlotte Close,
 * Caversham, Reading, Berkshire, United Kingdom RG4 7BY.
 *
 * This Original Work is licensed under the European Union Public Licence (EUPL) 
 * v.1.2 and is subject to its terms as set out below.
 *
 * If a copy of the EUPL was not distributed with this file, You can obtain
 * one at https://opensource.org/licenses/EUPL-1.2.
 *
 * The 'Compatible Licences' set out in the Appendix to the EUPL (as may be
 * amended by the European Commission) shall be deemed incompatible for
 * the purposes of the Work and the provisions of the compatibility
 * clause in Article 5 of the EUPL shall not apply.
 * 
 * If using the Work as, or as part of, a network application, by 
 * including the attribution notice(s) required under Article 5 of the EUPL
 * in the end user terms of the application under an appropriate heading, 
 * such notice(s) shall fulfill the requirements of that article.
 * ********************************************************************* */


%include std_vector.i
%include std_string.i
%include various.i

%typemap(jni) (unsigned char *UCHAR, long LONG) "jbyteArray"
%typemap(jtype) (unsigned char *UCHAR, long LONG) "byte[]"
%typemap(jstype) (unsigned char *UCHAR, long LONG) "byte[]"
%typemap(in) (unsigned char *UCHAR, long LONG) {
	if ($input != NULL) {
	    // Get the number of bytes in the byte array.
		$2 = jenv->GetArrayLength($input);
		// Allocate memory for the destination byte array used internally by
		// the data set. This memory is required for the lifetime of the data
		// set.
		$1 = (unsigned char*)malloc($2);
		if ($1 == NULL) {
		    SWIG_JavaThrowException(
		        jenv,
		        SWIG_JavaRuntimeException,
		        "Failed to allocate memory to copy the input byte array.");
		    return $null;
		}
		// Attempt to get a pointer to the data within the jbyteArray.
		jbyte* data = jenv->GetByteArrayElements($input, NULL);
		if (data == NULL) {
		    SWIG_JavaThrowException(
		        jenv,
		        SWIG_JavaRuntimeException,
		        "Failed to obtain pointer to the input byte array.");
		    return $null;
		}
        // Copy the input byte array to the destination and release the
        // reference to source pointer.
        memcpy($1, data, $2);
        jenv->ReleaseByteArrayElements($input, data, JNI_ABORT);
	}
	else {
	    // Let the underlying C implementation throw the null pointer exception.
		$1 = (unsigned char*)NULL;
		$2 = 0;
	}
}

%typemap(javain) (unsigned char *UCHAR, long LONG) "$javainput"

/* Prevent default freearg typemap from being used */
%typemap(freearg) (unsigned char *UCHAR, long LONG) ""

%apply (unsigned char *UCHAR, long LONG) { (unsigned char data[], long length) };

/* Use byte correctly where methods would otherwise not take a proper type. */
%typemap(jni) (unsigned char UCHAR) "int"
%typemap(jtype) (unsigned char UCHAR) "int"
%typemap(jstype) (unsigned char UCHAR) "byte"
%typemap(javain) (unsigned char UCHAR) "(int)$javainput"
%typemap(in) (unsigned char UCHAR) {
    $1 = (byte)$input;
  }
%typemap(out) (unsigned char UCHAR) "$result = (int)$1;"
%typemap(javaout) (unsigned char UCHAR) {
    return (byte)$jnicall;
  }
/* Prevent default freearg typemap from being used */
%typemap(freearg) (unsigned char UCHAR) ""
%apply (unsigned char UCHAR) { (byte) };

%define autocloseable(name)
%typemap(javainterfaces) name "AutoCloseable";
%typemap(javacode) name %{
  @Override
  public void close() {
    this.delete();
  }
%}
%enddef

%define nofinalize(name)
%typemap(javafinalize) name %{%}
%enddef


autocloseable(EvidenceBase);
autocloseable(Value);
autocloseable(std::map);
autocloseable(std::vector);
%extend std::vector {
    %typemap(javainterfaces) std::vector "AutoCloseable, java.util.RandomAccess";
};
autocloseable(ResultsBase);
autocloseable(EngineBase);

nofinalize(ResultsBase)
nofinalize(EvidenceBase);
nofinalize(Value);
nofinalize(std::map);
nofinalize(std::vector);
