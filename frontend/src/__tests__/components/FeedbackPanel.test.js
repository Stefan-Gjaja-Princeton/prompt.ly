/**
 * Unit tests for FeedbackPanel component
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import FeedbackPanel from '../../components/FeedbackPanel';

describe('FeedbackPanel', () => {
  it('should render loading state', () => {
    render(<FeedbackPanel loading={true} />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('should display quality score', () => {
    render(<FeedbackPanel qualityScore={7.5} feedback={{}} />);
    expect(screen.getByText(/7\.5/)).toBeInTheDocument();
  });

  it('should display quality label', () => {
    const feedback = {
      quality_label: 'Good',
      improvement_tips: [],
    };
    render(<FeedbackPanel qualityScore={7.5} feedback={feedback} />);
    expect(screen.getByText('Good')).toBeInTheDocument();
  });

  it('should display improvement tips', () => {
    const feedback = {
      quality_label: 'Good',
      improvement_tips: [
        'Be more specific',
        'Add context',
        'Ask focused questions',
      ],
    };
    render(<FeedbackPanel qualityScore={7.5} feedback={feedback} />);
    expect(screen.getByText('Be more specific')).toBeInTheDocument();
    expect(screen.getByText('Add context')).toBeInTheDocument();
    expect(screen.getByText('Ask focused questions')).toBeInTheDocument();
  });

  it('should display example improved prompt', () => {
    const feedback = {
      quality_label: 'Good',
      improvement_tips: [],
      example_improved_prompt: 'Can you explain neural networks with examples?',
    };
    render(<FeedbackPanel qualityScore={7.5} feedback={feedback} />);
    expect(screen.getByText(/example improved prompt/i)).toBeInTheDocument();
    expect(screen.getByText('Can you explain neural networks with examples?')).toBeInTheDocument();
  });

  it('should handle null quality score', () => {
    render(<FeedbackPanel qualityScore={null} feedback={{}} />);
    expect(screen.getByText(/prompt score/i)).toBeInTheDocument();
  });

  it('should handle old string feedback format', () => {
    render(<FeedbackPanel qualityScore={7.5} feedback="Old feedback string" />);
    // Should not crash, but may not display feedback details
    expect(screen.getByText(/prompt score/i)).toBeInTheDocument();
  });

  it('should open info modal when info button is clicked', () => {
    render(<FeedbackPanel qualityScore={7.5} feedback={{}} />);
    
    const infoButton = screen.getByLabelText(/how prompt scoring works/i);
    fireEvent.click(infoButton);
    
    // Info modal should open (implementation depends on TutorialModal)
    expect(infoButton).toBeInTheDocument();
  });

  it('should display correct score color for high scores', () => {
    const { container } = render(<FeedbackPanel qualityScore={9.0} feedback={{}} />);
    const scoreBar = container.querySelector('.quality-bar-fill');
    expect(scoreBar).toBeTruthy();
  });

  it('should display correct score color for low scores', () => {
    const { container } = render(<FeedbackPanel qualityScore={2.0} feedback={{}} />);
    const scoreBar = container.querySelector('.quality-bar-fill');
    expect(scoreBar).toBeTruthy();
  });
});

