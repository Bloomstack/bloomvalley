frappe.provide("bv");

bv.SingleItemCart = class SingleItemCart {
  constructor(config) {
    this.sales_order_name = null;
    this.grand_total = null;
    this.custom_fields = {};

    this.config = Object.assign({
      item_code: undefined // Required.
    }, config);

    if (!config.item_code) {
      throw new Error("Invalid Single Item Cart setup. You must provide an item_code key.")
    }

    frappe.call({
      method: "erpnext.shopping_cart.product_info.get_product_info_for_website",
      args: {
        item_code: config.item_code,
        skip_quotation_creation: true
      },
      callback: (r) => {
        if ( !r.exc ) {
          this.item = r.message.product_info;
          if ( config.on_item_info ) {
            config.on_item_info(this.item);
          }
        }
      }
    })
  }

  setContactInfo(contact_info) {
    this.contact_info = contact_info;
  }

  setCouponCode(coupon_code) {
    this.coupon_code = coupon_code;
  }

  setCustomField(field, value) {
    this.custom_fields[field] = value;
  }

  handle_success(res) {
    window.location.href = res.gateway_url;

		const success_dialog = new frappe.ui.Dialog({
			title: this.success_title || __("Loading gateway"),
			secondary_action: () => {
				window.location.href = "/";
			}
		});

		success_dialog.show();
		const success_message = __("Please wait...");
		success_dialog.set_message(success_message);
  }

  async purchase() {
    try {
      const res = await frappe.call({
        method: "bloomvalley.cart.checkout_one",
        args: {
          item_code: this.config.item_code,
          contact_info: this.contact_info,
          coupon_code: this.coupon_code || "",
          sales_order_name: this.sales_order,
          payment_gateway: this.config.payment_gateway,
          currency: this.config.currency,
          success_url: this.config.success_url,
          custom_fields: this.custom_fields
        }
      });

      if ( !res.exc ) {
        const result = res.message;
        if ( result.sales_order_name ) {
          this.sales_order_name = result.sales_order_name;
          this.grand_total = result.grand_total
        }

        const next = () => {
          this.handle_success(res.message);
        }

        return {
          success: true,
          next
        }
      }

    } catch (err) {
      console.error(err);
      console.log("Error while trying to purchase item...");
      return {
        success: false
      }
    }
  }
}