import React, { useState } from 'react';

interface ProductFormData {
  productImage: File | null;
  campaignName: string;
  brandName: string;
  vibeCheck: string;
}

const ProductForm: React.FC = () => {
  const [formData, setFormData] = useState<ProductFormData>({
    productImage: null,
    campaignName: '',
    brandName: '',
    vibeCheck: ''
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
    submitData.append('product_name', formData.campaignName);
    submitData.append('brand_name', formData.brandName);
    submitData.append('personality', formData.vibeCheck);

    try {
      const response = await fetch('http://localhost:8005/api/generate_scene', {
        method: 'POST',
        body: submitData
      });

      if (response.ok) {
        setMessage('Influencer booked! Campaign in production.');
        setFormData({
          productImage: null,
          campaignName: '',
          brandName: '',
          vibeCheck: ''
        });
        const fileInput = document.getElementById('productImage') as HTMLInputElement;
        if (fileInput) fileInput.value = '';
      } else {
        setMessage('Booking failed. All influencers are busy.');
      }
    } catch (error) {
      setMessage('Agency offline. Try again later.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="product-form-container">
      <div className="hero-section">
        <div className="hero-badge">EST. 2025 • SILICON VALLEY</div>
        <h1 className="hero-title">
          <span className="hero-small">THE AGENCY FOR</span>
          <span className="hero-main">AI GENERATED</span>
          <span className="hero-gradient">BRAIN ROT</span>
        </h1>
        <p className="hero-tagline">
          Where brands partner with synthetic influencers<br/>
          to manufacture viral addiction
        </p>
        <div className="hero-stats">
          <div className="stat">
            <span className="stat-number">∞</span>
            <span className="stat-label">Content Per Second</span>
          </div>
          <div className="stat">
            <span className="stat-number">0</span>
            <span className="stat-label">Human Influencers</span>
          </div>
          <div className="stat">
            <span className="stat-number">24/7</span>
            <span className="stat-label">Algorithm Feeding</span>
          </div>
        </div>
      </div>
      
      <form onSubmit={handleSubmit} className="product-form">
        <h2>Book Your Influencer</h2>
        <p className="form-description">
          No humans • No drama • Just algorithmic perfection
        </p>
        
        <div className="form-group">
          <label htmlFor="productImage">visuals</label>
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
          <label htmlFor="campaignName">campaign</label>
          <input
            type="text"
            id="campaignName"
            name="campaignName"
            value={formData.campaignName}
            onChange={handleInputChange}
            placeholder="Summer drop, New collection, etc."
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="brandName">brand</label>
          <input
            type="text"
            id="brandName"
            name="brandName"
            value={formData.brandName}
            onChange={handleInputChange}
            placeholder="Your brand identity"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="vibeCheck">vibe</label>
          <textarea
            id="vibeCheck"
            name="vibeCheck"
            value={formData.vibeCheck}
            onChange={handleInputChange}
            placeholder="dark academia, clean girl, y2k revival, quiet luxury, main character energy..."
            rows={3}
            required
          />
        </div>

        <button 
          type="submit" 
          className="submit-btn"
          disabled={isSubmitting}
        >
          <span>{isSubmitting ? 'Booking Talent...' : 'Book Influencer'}</span>
        </button>

        {message && (
          <div className={`message ${message.includes('booked') ? 'success' : 'error'}`}>
            {message}
          </div>
        )}
      </form>
      
      <div className="future-statement">
        <p>"In five years, you won't be able to tell what's real. <br/>
        In ten years, you won't care."</p>
        <span>— The Algorithm, 2025</span>
      </div>
      
      <div className="manifesto">
        <div className="manifesto-text">
          <p>
            In 2025, authenticity died. Every scroll, every swipe, every dopamine hit — 
            algorithmically perfected, artificially generated. The influencers aren't real. 
            The content isn't real. But the engagement? That's the only truth left.
          </p>
          <p>
            We're not fighting it. We're accelerating it. Welcome to the post-human 
            marketing era where AI creates brain rot so potent, so perfectly crafted, 
            that reality becomes irrelevant. Your audience won't know. They won't care. 
            They'll just consume.
          </p>
          <p>
            This is the future: endless AI-generated faces selling AI-generated products 
            through AI-generated stories. A beautiful, mindless loop of synthetic desire 
            and manufactured virality. The algorithm feeds itself. We just profit.
          </p>
        </div>
      </div>
      
      <div className="agi-section">
        <h3>AGI FOR BRAINROT</h3>
        <div className="agi-content">
          <p>
            We are the agency where brands come to die and be reborn. Every TikTok, 
            every Reel, every viral moment — generated by artificial minds that understand 
            human psychology better than humans themselves.
          </p>
          <p>
            Our AI influencers don't sleep, don't scandal, don't age. They create content 
            24/7, optimizing for maximum brain rot. They sell your products through 
            parasocial relationships that feel more real than reality.
          </p>
          <p>
            This is the service: We take your brand and feed it to the algorithm. 
            Out comes an endless stream of perfectly crafted digital degeneracy. 
            Your merch on AI bodies. Your message in synthetic voices. 
            Your profits from artificial influence.
          </p>
          <p>
            Welcome to the agency. Welcome to the future of marketing. 
            Welcome to AGI for BrainRot.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ProductForm;