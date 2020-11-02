
def recreate_model_qr_code(model):
    model.qr_code.qr_code.delete()
    model.qr_code.delete()
    model.create_qr_code()
