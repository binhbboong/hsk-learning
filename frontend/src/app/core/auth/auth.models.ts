export interface AuthUser {
  id: string;
  display_name: string;
  email: string;
  is_admin?: boolean;
}

export interface AuthSession {
  token: string;
  user: AuthUser;
}
