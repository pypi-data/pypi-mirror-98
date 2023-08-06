module skyline
integer:: dof_total
integer:: nnz
integer,allocatable::m(:)
integer ,allocatable::diag_loc(:)
real*8, allocatable:: a(:)

contains
subroutine init(mm, dof)
	integer, intent(in):: dof
	integer, intent(in):: mm(dof)
	integer:: n,i
	allocate(m(dof))
	allocate(diag_loc(dof))
	dof_total=dof
	m=mm
	
	diag_loc(1)=1
	do i=2,dof
		diag_loc(i)=diag_loc(i-1)+i-m(i-1)
	end do
	
	
	nnz = diag_loc(dof)+dof-m(dof)
	
	allocate(a(nnz))
	a = 0.0d0
end subroutine

subroutine add_value(i,j,v)
	integer, intent(in):: i,j
	real*8, intent(in):: v
	a(find_loc(i,j))=a(find_loc(i,j))+v
end subroutine

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
integer function find_loc(i,j)
  integer ,intent(in)::i,j
 find_loc=j-i+diag_loc(j)
end function
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

subroutine decompose()
real*8,allocatable:: g(:)
integer::n


n=size(diag_loc)



do j=2,n
  allocate (g(m(j):j))
  g(m(j))=a(find_loc(m(j),j))
  do i=m(j)+1,j-1
    g(i)=a(find_loc(i,j))
    m_m=max(m(i),m(j))
    do k=m_m,i-1
      g(i)=g(i)-a(find_loc(k,i))*g(k)
    end do
  end do
  do i=m(j),j-1
     a(find_loc(i,j))=g(i)/a(diag_loc(i))
  end do
  do k=m(j),j-1
      a(diag_loc(j))=a(diag_loc(j))-a(find_loc(k,j))*g(k)
  end do
  deallocate(g)
  if (a(diag_loc(j))<=0.0d0) then
    print *, '**** The matrix is singular! ****'
    !print *, ' Nonpositive pivot for equation =',j
    print *,' Press any key to exit ....'
    read * 
    stop
  end if
end do
end subroutine
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
subroutine solve(x, dof)
   integer, intent(in):: dof
   real*8,intent(inout)::x(dof)
   real*8::x_bar(dof)
   integer::n,i,k
   n=dof
   do i=2,n
     do k=m(i),i-1
         x(i)=x(i)-a(find_loc(k,i))*x(k)
     end do
   end do
   do i=1,n
       x_bar(i)=x(i)/a(diag_loc(i))
   end do
   
   x(n)=x_bar(n)
   do i=n,2,-1
     do k=m(i),i-1
       x_bar(k)=x_bar(k)-a(find_loc(k,i))*x(i)
     end do
     x(i-1)=x_bar(i-1)
   end do
end subroutine
!!!!!!!!!!!!!!!!!!!!!!!!!!!!

subroutine to_dense(d)
	real*8, intent(inout):: d(:,:)
		do i=1,dof_total
		do j = m(i),i
			d(j,i) = a(find_loc(j,i))
			d(i,j) = d(j,i)
		end do
	end do
end subroutine

subroutine get_value(i,j,v)
	integer, intent(in)::i,j
	real*8, intent(out):: v
	v=a(find_loc(i,j))
end subroutine

subroutine set_value(i,j,v)
	integer, intent(in)::i,j
	real*8, intent(in):: v
	a(find_loc(i,j))=v
end subroutine

subroutine set(v)
  real*8, intent(in):: v
  a = v
end subroutine
end module