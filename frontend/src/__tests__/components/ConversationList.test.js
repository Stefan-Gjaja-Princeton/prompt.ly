/**
 * Unit tests for ConversationList component
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ConversationList from '../../components/ConversationList';

describe('ConversationList', () => {
  const mockConversations = [
    {
      conversation_id: 'conv-1',
      title: 'Test Conversation 1',
      message_count: 5,
      updated_at: new Date().toISOString(),
    },
    {
      conversation_id: 'conv-2',
      title: 'Test Conversation 2',
      message_count: 3,
      updated_at: new Date(Date.now() - 86400000).toISOString(), // Yesterday
    },
  ];

  const defaultProps = {
    conversations: [],
    currentConversationId: null,
    onSelectConversation: jest.fn(),
    onCreateNew: jest.fn(),
    onDeleteConversation: jest.fn(),
  };

  it('should render empty state when no conversations', () => {
    render(<ConversationList {...defaultProps} />);
    expect(screen.getByText('No conversations yet')).toBeInTheDocument();
  });

  it('should render loading state', () => {
    render(<ConversationList {...defaultProps} loading={true} />);
    expect(screen.getByText(/loading conversations/i)).toBeInTheDocument();
  });

  it('should render list of conversations', () => {
    render(<ConversationList {...defaultProps} conversations={mockConversations} />);
    expect(screen.getByText('Test Conversation 1')).toBeInTheDocument();
    expect(screen.getByText('Test Conversation 2')).toBeInTheDocument();
  });

  it('should display message count', () => {
    render(<ConversationList {...defaultProps} conversations={mockConversations} />);
    expect(screen.getByText('5 messages')).toBeInTheDocument();
    expect(screen.getByText('3 messages')).toBeInTheDocument();
  });

  it('should display singular message count', () => {
    const singleMessageConv = [{
      conversation_id: 'conv-1',
      title: 'Test',
      message_count: 1,
      updated_at: new Date().toISOString(),
    }];
    render(<ConversationList {...defaultProps} conversations={singleMessageConv} />);
    expect(screen.getByText('1 message')).toBeInTheDocument();
  });

  it('should call onSelectConversation when conversation is clicked', () => {
    const onSelectConversation = jest.fn();
    render(
      <ConversationList
        {...defaultProps}
        conversations={mockConversations}
        onSelectConversation={onSelectConversation}
      />
    );
    
    fireEvent.click(screen.getByText('Test Conversation 1'));
    expect(onSelectConversation).toHaveBeenCalledWith('conv-1');
  });

  it('should highlight active conversation', () => {
    const { container } = render(
      <ConversationList
        {...defaultProps}
        conversations={mockConversations}
        currentConversationId="conv-1"
      />
    );
    
    const activeItem = container.querySelector('.conversation-item.active');
    expect(activeItem).toBeTruthy();
    expect(activeItem).toHaveTextContent('Test Conversation 1');
  });

  it('should call onCreateNew when plus button is clicked', () => {
    const onCreateNew = jest.fn();
    render(<ConversationList {...defaultProps} onCreateNew={onCreateNew} />);
    
    const plusButton = screen.getByTitle('Start new conversation');
    fireEvent.click(plusButton);
    
    expect(onCreateNew).toHaveBeenCalledTimes(1);
  });

  it('should disable plus button when isNewConversation is true', () => {
    const { container } = render(<ConversationList {...defaultProps} isNewConversation={true} />);
    
    const plusButton = container.querySelector('.new-conversation-btn');
    expect(plusButton).toBeDisabled();
  });

  it('should call onDeleteConversation when delete button is clicked', () => {
    const onDeleteConversation = jest.fn();
    render(
      <ConversationList
        {...defaultProps}
        conversations={mockConversations}
        onDeleteConversation={onDeleteConversation}
      />
    );
    
    const deleteButtons = screen.getAllByRole('button', { name: /delete/i });
    fireEvent.click(deleteButtons[0]);
    
    expect(onDeleteConversation).toHaveBeenCalledWith('conv-1');
  });

  it('should not trigger onSelectConversation when delete button is clicked', () => {
    const onSelectConversation = jest.fn();
    const onDeleteConversation = jest.fn();
    render(
      <ConversationList
        {...defaultProps}
        conversations={mockConversations}
        onSelectConversation={onSelectConversation}
        onDeleteConversation={onDeleteConversation}
      />
    );
    
    const deleteButtons = screen.getAllByRole('button', { name: /delete/i });
    fireEvent.click(deleteButtons[0]);
    
    expect(onDeleteConversation).toHaveBeenCalled();
    expect(onSelectConversation).not.toHaveBeenCalled();
  });

  it('should format dates correctly', () => {
    const today = new Date().toISOString();
    const yesterday = new Date(Date.now() - 86400000).toISOString();
    const weekAgo = new Date(Date.now() - 7 * 86400000).toISOString();
    
    const conversations = [
      { conversation_id: '1', title: 'Today', updated_at: today, message_count: 1 },
      { conversation_id: '2', title: 'Yesterday', updated_at: yesterday, message_count: 1 },
      { conversation_id: '3', title: 'Week Ago', updated_at: weekAgo, message_count: 1 },
    ];
    
    const { container } = render(<ConversationList {...defaultProps} conversations={conversations} />);
    
    // Check that date spans contain the formatted dates
    const dateSpans = container.querySelectorAll('.conversation-date');
    const dateTexts = Array.from(dateSpans).map(span => span.textContent);
    expect(dateTexts.some(text => text.includes('Today'))).toBe(true);
    expect(dateTexts.some(text => text.includes('Yesterday'))).toBe(true);
  });

  it('should display default title when conversation has no title', () => {
    const noTitleConv = [{
      conversation_id: 'conv-1',
      title: null,
      message_count: 1,
      updated_at: new Date().toISOString(),
    }];
    render(<ConversationList {...defaultProps} conversations={noTitleConv} />);
    expect(screen.getByText('New Conversation')).toBeInTheDocument();
  });
});

