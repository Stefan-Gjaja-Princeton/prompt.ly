import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { LogOut, User } from "lucide-react";
import "./UserHeader.css";

const UserHeader = () => {
  const { user, logout, getAccessTokenSilently } = useAuth0();

  if (!user) return null;

  const handleLogout = () => {
    logout({ logoutParams: { returnTo: window.location.origin } });
  };

  return (
    <div className="user-header">
      <div className="user-info">
        {user.picture ? (
          <img src={user.picture} alt={user.name} className="user-avatar" />
        ) : (
          <div className="user-avatar-placeholder">
            <User size={20} />
          </div>
        )}
        <div className="user-details">
          <span className="user-name">{user.name}</span>
          <span className="user-email">{user.email}</span>
        </div>
      </div>
      <button className="logout-button" onClick={handleLogout} title="Logout">
        <LogOut size={18} />
      </button>
    </div>
  );
};

export default UserHeader;
