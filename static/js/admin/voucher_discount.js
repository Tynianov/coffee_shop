jQuery(document).ready(function ($) {
    const freeItemRow = '.field-free_item';
    const amountRow = '.field-amount';
    const purchaseRow = '.field-purchase_count';
    const voucherTypeSelect = '#id_type';
    const discountTypeSelect = '#id_discount';

    function initDisplay(){
        if ($(discountTypeSelect).val() !== 'free_item'){
            $(freeItemRow).hide();
        }
        else {
            $(amountRow).hide();
            if ($(voucherTypeSelect).val() !== 'min_purchase_amount'){
                $(purchaseRow).hide();
            }
        }
    }

    function voucherTypeOnSelectChange(element){

        if (element.val() === 'min_purchase_amount'){
            $(purchaseRow).show();
        }
        else {
            $(purchaseRow).hide();
        }
    }

    function discountTypeOnSelectChange(element){
        if (element.val() === 'free_item'){
            $(freeItemRow).show();
            $(amountRow).hide();
            if ($(voucherTypeSelect).val() !== 'min_purchase_amount'){
                $(purchaseRow).hide();
            }
        }
        else{
            $(freeItemRow).hide();
            $(amountRow).show();
            $(purchaseRow).show();
        }
    }

    $(document).ready(function () {
        initDisplay();
        $(document).on('change', voucherTypeSelect, function (e){
            const $this = $(e.target);
            voucherTypeOnSelectChange($this)
        });
        $(document).on('change', discountTypeSelect, function (e){
            const $this = $(e.target);
            discountTypeOnSelectChange($this)
        });
    });
});