frappe.provide("bv");

bv.extractInputFields = ($el) => {
  const fields = {};
  $el.find('[name]').each(function () {
    Reflect.set(fields, $(this).attr('name'), $(this).val());
  });
  return fields;
}

/**
 * Triggers a callback when the location hash changes.
 * @param {string} hash 
 * @param {function} callback 
 */
bv.on_hash = (hash, callback) => {
  const testHash = () => {
    if ( window.location.hash.indexOf(hash) > -1) {
      callback(hash);
    }
  }

  window.addEventListener("hashchange", testHash);
  testHash();
}

/**
 * Initializes a simple validation/required fields mechanism to validate field values.
 * The provided callback will be called every time a field value changes which is marked
 * as required.
 * @param {jQuery} $form 
 * @param {function} validationCallback 
 */
bv.initForm = ($form, validationCallback, fieldValidationCallback) => {
  const $requiredFields = $form.find('input');
  const isValid = () => {
    let invalidFields  = $requiredFields.length;
    $requiredFields.each(function() {
      if ( $(this).is(":valid") ) {
        invalidFields--;
      }
    })  
    const result = invalidFields == 0;
    return result;
  }

  $requiredFields.each(function() {
    $(this).change(function() {
      fieldValidationCallback($(this));
      validationCallback(isValid());
    });
  });

  validationCallback(isValid());
}

bv.store = (key, defaultValue, set) => {
  const value = localStorage.getItem(key);
  if ( !set && value ) {
    return JSON.parse(value);
  } else if (set || defaultValue) {
    if ( defaultValue === undefined ) {
      localStorage.removeItem(key);
    } else {
      localStorage.setItem(key, JSON.stringify(defaultValue));
    }
    return defaultValue;
  }
}