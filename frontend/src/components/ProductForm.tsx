import React, { useState } from 'react';

interface ProductFormData {
  productImage: File | null;
  productName: string;
  brandName: string;
  personality: string;
}

const ProductForm: React.FC = () => {
  const [formData, setFormData] = useState<ProductFormData>({
    productImage: null,
    productName: '',
    brandName: '',
    personality: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState('');

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFormData({ ...formData, productImage: e.target.files[0] });
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.productImage) {
      setMessage('Please upload a product image');
      return;
    }

    setIsSubmitting(true);
    setMessage('');

    const submitData = new FormData();
    submitData.append('product_image', formData.productImage);
    submitData.append('product_name', formData.productName);
    submitData.append('brand_name', formData.brandName);
    submitData.append('personality', formData.personality);

    try {
      const response = await fetch('http://localhost:8000/api/submit-product', {
        method: 'POST',
        body: submitData
      });

      if (response.ok) {
        setMessage('Product successfully submitted to AI Agency!');
        setFormData({
          productImage: null,
          productName: '',
          brandName: '',
          personality: ''
        });
        const fileInput = document.getElementById('productImage') as HTMLInputElement;
        if (fileInput) fileInput.value = '';
      } else {
        setMessage('Failed to submit product. Please try again.');
      }
    } catch (error) {
      setMessage('Error connecting to backend. Please ensure the server is running.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="product-form-container">
      <form onSubmit={handleSubmit} className="product-form">
        <h2>Partner with Digital Influencers</h2>
        <p className="form-description">
          Submit your product details and let our AI Agency create compelling content 
          for digital influencers to promote your brand.
        </p>
        
        <div className="form-group">
          <label htmlFor="productImage">Product Image *</label>
          <input
            type="file"
            id="productImage"
            accept="image/*"
            onChange={handleImageChange}
            required
          />
          {formData.productImage && (
            <div className="image-preview">
              <img 
                src={URL.createObjectURL(formData.productImage)} 
                alt="Product preview" 
              />
            </div>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="productName">Product Name *</label>
          <input
            type="text"
            id="productName"
            name="productName"
            value={formData.productName}
            onChange={handleInputChange}
            placeholder="Enter your product name"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="brandName">Brand Name *</label>
          <input
            type="text"
            id="brandName"
            name="brandName"
            value={formData.brandName}
            onChange={handleInputChange}
            placeholder="Enter your brand name"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="personality">Brand Personality *</label>
          <textarea
            id="personality"
            name="personality"
            value={formData.personality}
            onChange={handleInputChange}
            placeholder="Describe your brand's personality (e.g., innovative, eco-friendly, luxurious, playful)"
            rows={4}
            required
          />
        </div>

        <button 
          type="submit" 
          className="submit-btn"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Submitting...' : 'Submit to AI Agency'}
        </button>

        {message && (
          <div className={`message ${message.includes('successfully') ? 'success' : 'error'}`}>
            {message}
          </div>
        )}
      </form>
    </div>
  );
};

export default ProductForm;