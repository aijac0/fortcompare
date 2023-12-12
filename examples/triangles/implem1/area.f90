subroutine compute_area
    use triangles
    implicit none

    ! Local variables
    real :: s

    ! Real triangles
    if (calc_real_triangle) then
        s = (t1(1) + t1(2) + t1(3)) * 0.5
        t1_area = sqrt(s * (s - t1(1)) * (s - t1(2)) * (s - t1(3)))
        s = (t2(1) + t2(2) + t2(3)) * 0.5
        t2_area = sqrt(s * (s - t2(1)) * (s - t2(2)) * (s - t2(3)))
        s = (t3(1) + t3(2) + t3(3)) * 0.5
        t3_area = sqrt(s * (s - t3(1)) * (s - t3(2)) * (s - t3(3)))
        output_real_triangle = "Computed"
    else
        output_real_triangle = "Requested to not compute"
    endif
   
    ! Integer triangles
    if (calc_int_triangle) then
        s = (int_t1(1) + int_t1(2) + int_t1(3)) * 0.5
        int_t1_area = sqrt(s * (s - int_t1(1)) * (s - int_t1(2)) * (s - int_t1(3)))
        s = (int_t2(1) + int_t2(2) + int_t2(3)) * 0.5
        int_t2_area = sqrt(s * (s - int_t2(1)) * (s - int_t2(2)) * (s - int_t2(3)))
        s = (int_t3(1) + int_t3(2) + int_t3(3)) * 0.5
        int_t3_area = sqrt(s * (s - int_t3(1)) * (s - int_t3(2)) * (s - int_t3(3)))
        output_int_triangle = "Computed"
    else
        output_int_triangle = "Requested to not compute"
    endif

    ! Real right triangles
    if (calc_real_right_triangle) then
        s = (right_t1(1) + right_t1(2) + right_t1(3)) * 0.5
        right_t1_area = sqrt(s * (s - right_t1(1)) * (s - right_t1(2)) * (s - right_t1(3)))
        s = (right_t2(1) + right_t2(2) + right_t2(3)) * 0.5
        right_t2_area = sqrt(s * (s - right_t2(1)) * (s - right_t2(2)) * (s - right_t2(3)))
        s = (right_t3(1) + right_t3(2) + right_t3(3)) * 0.5
        right_t3_area = sqrt(s * (s - right_t3(1)) * (s - right_t3(2)) * (s - right_t3(3)))
        output_real_right_triangle = "Computed"
    else
        output_real_right_triangle = "Requested to not compute"
    endif

    ! Integer right triangles
    if (calc_int_right_triangle) then
        s = (int_right_t1(1) + int_right_t1(2) + int_right_t1(3)) * 0.5
        int_right_t1_area = sqrt(s * (s - int_right_t1(1)) * (s - int_right_t1(2)) * (s - int_right_t1(3)))
        s = (int_right_t2(1) + int_right_t2(2) + int_right_t2(3)) * 0.5
        int_right_t2_area = sqrt(s * (s - int_right_t2(1)) * (s - int_right_t2(2)) * (s - int_right_t2(3)))
        s = (int_right_t3(1) + int_right_t3(2) + int_right_t3(3)) * 0.5
        int_right_t3_area = sqrt(s * (s - int_right_t3(1)) * (s - int_right_t3(2)) * (s - int_right_t3(3)))
        output_int_right_triangle = "Computed"
    else
        output_int_right_triangle = "Requested to not compute"
    endif

end subroutine