begin
  integer k;
  integer function F(n);
    begin
      integer n;
      if n<=0 then F:=1
      else F:=n*F(n-1)
    end;
  integer function X(x);
    begin
        integer x;
        if x>0 then x:=x-1
        else x:=x-2
      /* hell*o world */
    end;
  read(m);
  k:=F(m);
  write(k)
end
