import {render, screen} from '@testing-library/react';
import App from './App';

test('renders lern react link', () => {
    render(<App />);
    const linkElement = screen.getByText(/lern react/i);
    expect(linkElement).toBeInTheDocument(); 
});