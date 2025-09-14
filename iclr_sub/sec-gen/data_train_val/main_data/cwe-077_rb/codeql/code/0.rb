class ImagePickerController < ApplicationController
  def pick
    image_name = params[:image_name]
    image = open(image_name)
    image_content = image.read
    render json: { image: image_content }
  end
end